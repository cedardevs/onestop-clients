import argparse
import json
import os

from onestop.extract.CsbExtractor import CsbExtractor
from onestop.KafkaConsumer import KafkaConsumer
from onestop.util.S3Utils import S3Utils

from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.point import Point
from onestop.schemas.geojsonSchemaClasses.point_type import PointType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum_algorithm import ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.temporal_bounding import TemporalBounding
from onestop.schemas.util.jsonEncoder import EnumEncoder, as_enum, EnumEncoderValue
from onestop.KafkaPublisher import KafkaPublisher
from spatial import script_generation, postgres_insert

def handler(key, value):
    '''
    Consumes message from psi-input-unknown, extracts geospatial data, uploads new payload to parsed-record topic in kafka, and uploads geospatial data to Postgres

    :param key: str
        kafka key
    :param value: dict
        information from item associated with the key

    :return: str
        returns response message from kafka
    '''
    print('Key:', key)
    print('Value: ' ,value)
    # Grabs the contents of the message and turns the dict string into a dictionary using json.loads
    try:
        content_dict = json.loads(value['content'], object_hook=as_enum)

        parsed_record = ParsedRecord().from_dict(content_dict)

        # Geospatial Extraction
        # Extract the bucket key for csb_extractor object initialization
        bucket_key = content_dict['discovery']['links'][0]['linkUrl'].split('.com/')[1]

        csb_extractor = CsbExtractor(su, bucket_key)
        if csb_extractor.is_csv(bucket_key):
            geospatial = csb_extractor.get_spatial_temporal_bounds('LON', 'LAT', 'TIME')
            begin_date, end_date = geospatial['temporal'][0], geospatial['temporal'][1]
            max_lon, max_lat, min_lon, min_lat = geospatial['geospatial'][2], geospatial['geospatial'][3], \
                                                 geospatial['geospatial'][0], geospatial['geospatial'][1]
            coords = csb_extractor.extract_coords(max_lon, max_lat, min_lon, min_lat)

            # Create spatial bounding types based on the given coords
            pointType = PointType('Point')
            point = Point(coordinates=coords[0], type=pointType)

            # Create temp bounding obj
            tempBounding = TemporalBounding(beginDate=begin_date, endDate=end_date)

            # Update parsed record object with geospatial data
            parsed_record.discovery.temporalBounding = tempBounding
            parsed_record.discovery.spatialBounding = point

            """
            # Insert data into postgres
            script = script_generation(coords[0], key)
            postgres_insert(script)
            """

        # update content dict
        parsed_record.type = value['type']
        content_dict = parsed_record.to_dict()
        # reformat Relationship field
        relationship_type = content_dict['relationships'][0]['type']['type']
        content_dict['relationships'][0]['type'] = relationship_type

        # reformat File Locations
        filelocation_type = content_dict['fileLocations']['type']['type']
        content_dict['fileLocations']['type'] = filelocation_type

        content_dict['discovery']['spatialBounding']['type'] = pointType.value

        # Transform content_dict to appropiate payload
        # cls=EnumEncoderValue argument looks for instances of Enum classes and extracts only the value of the Enum
        content_dict = json.dumps(content_dict, cls=EnumEncoderValue)
        content_dict = json.loads(content_dict)

        # Produce new information to kafka
        kafka_publisher = KafkaPublisher("scripts/config/kafka-publisher-config-dev.yml")
        metadata_producer = kafka_publisher.connect()
        collection_id = parsed_record.relationships[0].id
        kafka_publisher.publish_granule(metadata_producer, collection_id, collection_id, content_dict)

    except:
        print('Invalid Format')


if __name__ == '__main__':
    # This is where helm will mount the config
    conf_loc = "/etc/config/config.yml"
    # this is where we are about to write the cred yaml
    cred_loc = "creds.yml"

    registry_user = os.environ.get("REGISTRY_USERNAME")
    registry_pwd = os.environ.get("REGISTRY_PASSWORD")
    access_key = os.environ.get("ACCESS_KEY")
    access_secret = os.environ.get("SECRET_KEY")

    f = open(cred_loc, "w+")

    # TODO revisit this when we make a standard that all scripts will follow
    # write creds to a file to avoid changing the python library
    s = """
    sandbox:
      access_key: {key}
      secret_key: {secret}
    registry:
      username: {user}
      password: {pw}
    """.format(key=access_key, secret=access_secret, user=registry_user, pw=registry_pwd)
    f.write(s)
    f.close()
    r = open(cred_loc, "r")

    su = S3Utils(conf_loc, cred_loc)
    kafka_consumer = KafkaConsumer(conf_loc)
    metadata_consumer = kafka_consumer.connect()
    kafka_consumer.consume(metadata_consumer, lambda k, v: handler(k, v))