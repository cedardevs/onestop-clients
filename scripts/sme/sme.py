from onestop.extract.CsbExtractor import CsbExtractor
from onestop.KafkaConsumer import KafkaConsumer
from onestop.util.S3Utils import S3Utils
import argparse
import json

from onestop.schemas.geojsonSchemaClasses.org.cedar.schemas.avro.geojson.point import Point
from onestop.schemas.geojsonSchemaClasses.point_type import PointType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum_algorithm import ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.temporal_bounding import TemporalBounding
from onestop.KafkaPublisher import KafkaPublisher
from spatial import script_generation, postgres_insert

def handler(key, value):
    print('Key:', key)
    print('Value: ' ,value)

    # Grabs the contents of the message and turns the dict string into a dictionary using json.loads
    content_dict = json.loads(value['content'])
    # Creates a checksum algorithm object based on contents of the message
    checksum_alg = ChecksumAlgorithm(content_dict['fileInformation']['checksums'][0]['algorithm'].strip('ChecksumAlgorithm.'))
    # assigns the checksum algorithm obj inside the content dict in order to used the from_dict method of the parsed record obj
    content_dict['fileInformation']['checksums'][0]['algorithm'] = checksum_alg
    parsed_record = ParsedRecord().from_dict(content_dict)



    # Geospatial Extraction
    # Extract the bucket key for csb_extractor object initialization
    bucket_key = content_dict['discovery']['links'][0]['linkUrl'].split('.com/')[1]

    csb_extractor = CsbExtractor(su, bucket_key)
    if csb_extractor.is_csv(bucket_key):
        geospatial = csb_extractor.get_spatial_temporal_bounds('LON', 'LAT', 'TIME')
        begin_date, end_date = geospatial['temporal'][0], geospatial['temporal'][1]
        max_lon , max_lat, min_lon, min_lat = geospatial['geospatial'][2],geospatial['geospatial'][3], geospatial['geospatial'][0], geospatial['geospatial'][1]
        coords = csb_extractor.extract_coords(max_lon , max_lat, min_lon, min_lat)

        # Create spatial bounding types based on the given coords
        pointType = PointType('Point')
        point = Point(coordinates=coords[0], type=pointType)

        # Create temp bounding obj
        tempBounding = TemporalBounding(beginDate=begin_date, endDate=end_date)

        # Update parsed record object with geospatial data
        parsed_record.discovery.temporalBounding= tempBounding
        parsed_record.discovery.spatialBounding= point

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
    content_dict['fileLocations']['optionalAttributes'] = {}

    # reformat Discovery
    content_dict['discovery']['keywords'] = []
    content_dict['discovery']['topicCategories'] = []
    content_dict['discovery']['acquisitionInstruments'] = []
    content_dict['discovery']['acquisitionOperations'] = []
    content_dict['discovery']['acquisitionPlatforms'] = []
    content_dict['discovery']['dataFormats'] = []
    content_dict['discovery']['responsibleParties']= []
    content_dict['discovery']['citeAsStatements'] = []
    content_dict['discovery']['crossReferences'] = []
    content_dict['discovery']['largerWorks'] = []
    content_dict['discovery']['legalConstraints'] = []
    content_dict['discovery']['dsmmAccessibility'], content_dict['discovery']['dsmmDataIntegrity'], content_dict['discovery']['dsmmDataQualityAssessment'], content_dict['discovery']['dsmmDataQualityAssurance'],content_dict['discovery']['dsmmDataQualityControlMonitoring'],content_dict['discovery']['dsmmPreservability']= 0,0,0,0,0,0
    content_dict['discovery']['dsmmProductionSustainability'], content_dict['discovery']['dsmmTransparencyTraceability'], content_dict['discovery']['dsmmUsability'],content_dict['discovery']['dsmmAverage'] = 0,0,0, 0.0
    content_dict['discovery']['services']= []
    content_dict['discovery']['spatialBounding']['type'] = 'Point'

    # Reformat File Information
    content_dict['fileInformation']['checksums'][0]['algorithm'] = 'MD5'

    # testing for granule only as of now
    if content_dict['type'] == 'granule':
        # Produce new information to kafka
        kafka_publisher = KafkaPublisher("scripts/config/kafka-publisher-config-dev.yml")
        metadata_producer = kafka_publisher.connect()
        collection_id = parsed_record.relationships[0].id
        kafka_publisher.publish_granule(metadata_producer, collection_id, collection_id, content_dict)


if __name__ == '__main__':
    su = S3Utils("scripts/config/aws-util-config-dev.yml", "scripts/config/credentials-template.yml")
    kafka_consumer = KafkaConsumer("scripts/config/kafka-publisher-config-dev.yml")
    metadata_consumer = kafka_consumer.connect()
    kafka_consumer.consume(metadata_consumer, lambda k, v: handler(k, v))