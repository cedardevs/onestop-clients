import json
import os
import yaml
import argparse

from onestop.extract.CsbExtractor import CsbExtractor
from onestop.KafkaConsumer import KafkaConsumer
from onestop.util.S3Utils import S3Utils

from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.point import Point
from onestop.schemas.geojsonSchemaClasses.point_type import PointType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.temporal_bounding import TemporalBounding
from onestop.schemas.util.jsonEncoder import as_enum, EnumEncoderValue
from onestop.KafkaPublisher import KafkaPublisher
#from spatial import script_generation, postgres_insert
from onestop.util.ClientLogger import ClientLogger

config_dict = {}

def handler(key, value, log_level = 'INFO'):
    '''
    Consumes message from psi-input-unknown, extracts geospatial data, uploads new payload to parsed-record topic in kafka, and uploads geospatial data to Postgres

    :param key: str
        kafka key
    :param value: dict
        information from item associated with the key

    :return: str
        returns response message from kafka
    '''
    # Grabs the contents of the message and turns the dict string into a dictionary using json.loads
    logger = ClientLogger.get_logger('sme.handler', log_level, False)
    logger.info('In Handler: key=%s value=%s'%(key, value))

    # This is an example for testing purposes.
    test_value = {
        "type": "granule",
        "content": "{"
                   "\"discovery\": {\n            "
                       "\"fileIdentifier\": \"92ade5dc-946d-11ea-abe4-0242ac120004\",\n            "
                       "\"links\": [\n                {\n                    "
                           "\"linkFunction\": \"download\",\n                    "
                           "\"linkName\": \"Amazon S3\",\n                    "
                           "\"linkProtocol\": \"HTTPS\",\n                    "
                           "\"linkUrl\": \"https://s3.amazonaws.com/nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\"\n                "
                       "}\n            ],\n            "
                       "\"parentIdentifier\": \"0fad03df-0805-434a-86a6-7dc42d68480f\",\n            "
                       "\"spatialBounding\": null,\n            "
                       "\"temporalBounding\": {\n                "
                          "\"beginDate\": \"2020-05-12T16:20:15.158Z\", \n                "
                          "\"endDate\": \"2020-05-12T16:21:51.494Z\"\n            "
                       "},\n            "
                          "\"title\": \"HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\"\n        "
                    "},\n        "
                    "\"fileInformation\": {\n  "
                       "\"checksums\": [{"
                           "\"algorithm\": \"MD5\","
                           "\"value\": \"44d2452e8bc2c8013e9c673086fbab7a\""
                       "}]\n, "
                       "\"optionalAttributes\":{},          "
                       "\"format\": \"HSD\",\n            "
                       "\"name\": \"HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\",\n            "
                       "\"size\": 208918\n        "
                    "},\n        "
                    "\"fileLocations\": {\n     "
                        "\"s3://nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\": {\n"
                            "\"optionalAttributes\":{},       "
                            "\"uri\":\"//nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\",   "
                            "\"asynchronous\": false,\n                "
                            "\"deleted\": false,\n                "
                            "\"lastModified\": 1589300890000,\n                "
                            "\"locality\": \"us-east-1\",\n                "
                            "\"restricted\": false,\n                "
                            "\"serviceType\": \"Amazon:AWS:S3\",\n                "
                            "\"type\": {\"__enum__\": \"FileLocationType.INGEST\"},\n                "
                            "\"uri\": \"s3://nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2\"\n                   "
                        "}\n        "
                   "},\n        "
                   "\"relationships\": [\n            {\n                "
                       "\"id\": \"0fad03df-0805-434a-86a6-7dc42d68480f\",\n                "
                       "\"type\": {\"__enum__\": \"RelationshipType.COLLECTION\"}           }\n        ]\n    "
                   "}",
        "contentType": "application/json",
        "method": "PUT",
        "source": "unknown",
        "operation": "ADD"
    }
    try:
        logger.debug('content: %s'%value['content'])
        content_dict = json.loads(value['content'], object_hook=as_enum) # this can fail if input values fail to map to avro ENUM values.
        logger.debug('content_dict: %s'%content_dict)
        parsed_record = ParsedRecord.from_dict(content_dict) # or ParsedRecord(**content_dict) # this can fail if input values fail to map to avro class values.
    except Exception as e:
        logger.exception('Skipping publishing kafka record, as could not json translate or turn into a ParsedRecord.', e)
        return

    # Geospatial Extraction
    bucket_key = content_dict['discovery']['links'][0]['linkUrl'].split('.com/')[1]
    logger.info("Bucket key="+bucket_key)
    if CsbExtractor.is_csv(bucket_key):
        logger.info('Extracting geospatial information')
        s3_session = su.connect("session", None, config_dict['s3_region'])
        sm_open_file = su.get_csv_s3(s3_session, config_dict['s3_bucket'], bucket_key)
        geospatial = CsbExtractor.get_spatial_temporal_bounds(sm_open_file, 'LON', 'LAT', 'TIME')
        begin_date, end_date = geospatial['temporal'][0], geospatial['temporal'][1]
        max_lon, max_lat, min_lon, min_lat = geospatial['geospatial'][2], geospatial['geospatial'][3], \
                                             geospatial['geospatial'][0], geospatial['geospatial'][1]
        coords = CsbExtractor.extract_coords(sm_open_file, max_lon, max_lat, min_lon, min_lat)

        # Create spatial bounding types based on the given coords
        pointType = PointType('Point')
        point = Point(coordinates=coords[0], type=pointType)

        # Create temp bounding obj
        logger.debug('beginDate=%s endDate=%s'%(begin_date, end_date))
        tempBounding = TemporalBounding(beginDate=begin_date, endDate=end_date)

        # Update parsed record object with geospatial data
        parsed_record.discovery.temporalBounding = tempBounding
        parsed_record.discovery.spatialBounding = point

        """
        # Insert data into postgres
        script = script_generation(coords[0], key)
        postgres_insert(script)
        """
    else:
        logger.info('Record not CSV - Skipping extracting geospatial information')

    # update content dict
    parsed_record.type = value['type']
    logger.debug('parsed_record: %s'%parsed_record)
    content_dict = parsed_record.to_dict()
    logger.debug('content_dict of parsed_record, to_dict(): %s'%content_dict)

    # Transform content_dict to appropriate payload
    # cls=EnumEncoderValue argument looks for instances of Enum classes and extracts only the value of the Enum
    content_dict = json.dumps(content_dict, cls=EnumEncoderValue)
    logger.debug('content_dict of json.dumps: %s'%content_dict)
    content_dict = json.loads(content_dict)
    logger.debug('content_dict of json.loads: %s'%content_dict)

    # Produce new information to publish to kafka, TODO: Be wary of cyclical publish/consuming here, since the consumer calls this handler.
    kafka_publisher = KafkaPublisher(**config_dict)
    metadata_producer = kafka_publisher.connect()
    collection_id = parsed_record.relationships[0].id
    kafka_publisher.publish_granule(metadata_producer, collection_id, content_dict)

if __name__ == '__main__':
    # Example command: python3 sme.py -conf /Users/whoever/repo/onestop-clients/scripts/config/combined_template.yml -cred /Users/whoever/repo/onestop-clients/scripts/config/credentials.yml
    #    python3 archive_client_integration.py -cred /Users/whoever/repo/onestop-clients/scripts/config/credentials.yml
    parser = argparse.ArgumentParser(description="Launches sme test")
    # Set default config location to the Helm mounted pod configuration location
    parser.add_argument('-conf', dest="conf", required=False, default='/etc/config/config.yml',
                        help="AWS config filepath")
    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Generate configuration dictionary
    conf_loc = args.pop('conf')
    with open(conf_loc) as f:
        config_dict.update(yaml.load(f, Loader=yaml.FullLoader))

    # Get credentials from passed in fully qualified path or ENV.
    cred_loc = args.pop('cred')
    if cred_loc is not None:
        with open(cred_loc) as f:
            creds = yaml.load(f, Loader=yaml.FullLoader)
        registry_username = creds['registry']['username']
        registry_password = creds['registry']['password']
        access_key = creds['sandbox']['access_key']
        access_secret = creds['sandbox']['secret_key']
    else:
        print("Using env variables for config parameters")
        registry_username = os.environ.get("REGISTRY_USERNAME")
        registry_password = os.environ.get("REGISTRY_PASSWORD")
        access_key = os.environ.get("ACCESS_KEY")
        access_secret = os.environ.get("SECRET_KEY")

    config_dict.update({
        'registry_username' : registry_username,
        'registry_password' : registry_password,
        'access_key' : access_key,
        'secret_key' : access_secret
    })

    su = S3Utils(**config_dict)

    kafka_consumer = KafkaConsumer(**config_dict)
    metadata_consumer = kafka_consumer.connect()
#    handler('', '', config_dict['log_level']) # For testing purposes
    kafka_consumer.consume(metadata_consumer, handler)