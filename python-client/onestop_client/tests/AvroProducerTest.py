
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

from confluent_kafka import avro
import os

def on_delivery(err, msg, obj):
    """
        Handle delivery reports served from producer.poll.
        This callback takes an extra argument, obj.
        This allows the original contents to be included for debugging purposes.
    """
    if err is not None:
        print('Message {} delivery failed for user {} with error {}'.format(
            obj.id, obj.name, err))
    else:
        print('Message {} successfully produced to {} [{}] at offset {}'.format(
            obj.id, msg.topic(), msg.partition(), msg.offset()))


if __name__ == '__main__':

    topic = "psi-registry-granule-parsed-changelog"
    bootstrap_servers = "localhost:30886"
    schema_registry = "http://localhost:32234"

    sr_conf = {'url': schema_registry}

    sr = CachedSchemaRegistryClient(sr_conf)
    ser = MessageSerializer(sr)

    base_conf = {
        'bootstrap.servers': bootstrap_servers,
        'schema.registry.url': schema_registry
         }

    producer = AvroProducer(base_conf)

    test = {
           	'type': 'granule',
           	'discovery': {
           		'fileIdentifier': 'gov.noaa.ngdc.mgg.photo_image:1195',
           		'parentIdentifier': 'gov.noaa.ngdc.mgg.photos:29',
           		'hierarchyLevelName': 'granule',
           		'doi': None,
           		'purpose': None,
           		'status': None,
           		'credit': None,
           		'title': 'Hawaii',
           		'alternateTitle': None,
           		'description': 'Aerial close-up of highway destruction. Unknown location (Hawaii).',
           		'keywords': [],
           		'topicCategories': [],
           		'temporalBounding': {
           			'beginDate': None,
           			'beginIndeterminate': None,
           			'endDate': None,
           			'endIndeterminate': None,
           			'instant': None,
           			'instantIndeterminate': None,
           			'description': None
           		},
           		'spatialBounding': {
           			'type': 'Point',
           			'coordinates': [-155.57, 19.91]
           		},
           		'isGlobal': False,
           		'acquisitionInstruments': [],
           		'acquisitionOperations': [],
           		'acquisitionPlatforms': [],
           		'dataFormats': [],
           		'links': [{
           			'linkName': 'Medium resolution image',
           			'linkProtocol': 'HTTPS',
           			'linkUrl': 'https://www.ngdc.noaa.gov/hazard/icons/med_res/128/b46d01-112.jpg',
           			'linkDescription': None,
           			'linkFunction': 'download'
           		}, {
           			'linkName': 'High resolution image',
           			'linkProtocol': 'HTTPS',
           			'linkUrl': 'https://www.ngdc.noaa.gov/hazard/img/200_res/128/b46d01-112.tif',
           			'linkDescription': None,
           			'linkFunction': 'download'
           		}],
           		'responsibleParties': [{
           			'individualName': None,
           			'organizationName': 'University of California at Berkeley',
           			'positionName': None,
           			'role': 'originator',
           			'email': None,
           			'phone': None
           		}],
           		'thumbnail': 'https://www.ngdc.noaa.gov/hazard/icons/med_res/128/b46d01-112.jpg',
           		'thumbnailDescription': 'Thumbnail image of photo',
           		'creationDate': None,
           		'revisionDate': None,
           		'publicationDate': None,
           		'citeAsStatements': [],
           		'crossReferences': [],
           		'largerWorks': [],
           		'useLimitation': None,
           		'legalConstraints': [],
           		'accessFeeStatement': None,
           		'orderingInstructions': None,
           		'edition': None,
           		'dsmmAccessibility': 0,
           		'dsmmDataIntegrity': 0,
           		'dsmmDataQualityAssessment': 0,
           		'dsmmDataQualityAssurance': 0,
           		'dsmmDataQualityControlMonitoring': 0,
           		'dsmmPreservability': 0,
           		'dsmmProductionSustainability': 0,
           		'dsmmTransparencyTraceability': 0,
           		'dsmmUsability': 0,
           		'dsmmAverage': 0.0,
           		'updateFrequency': None,
           		'presentationForm': None,
           		'services': []
           	},
           	'analysis': {
           		'identification': {
           			'fileIdentifierExists': True,
           			'fileIdentifierString': 'gov.noaa.ngdc.mgg.photo_image:1195',
           			'doiExists': False,
           			'doiString': None,
           			'parentIdentifierExists': True,
           			'parentIdentifierString': 'gov.noaa.ngdc.mgg.photos:29',
           			'hierarchyLevelNameExists': True,
           			'matchesIdentifiers': True
           		},
           		'titles': {
           			'titleExists': True,
           			'titleCharacters': 6,
           			'alternateTitleExists': False,
           			'alternateTitleCharacters': 0,
           			'titleFleschReadingEaseScore': 36.62000000000003,
           			'alternateTitleFleschReadingEaseScore': None,
           			'titleFleschKincaidReadingGradeLevel': 8.400000000000002,
           			'alternateTitleFleschKincaidReadingGradeLevel': None
           		},
           		'description': {
           			'descriptionExists': True,
           			'descriptionCharacters': 66,
           			'descriptionFleschReadingEaseScore': 23.00000000000003,
           			'descriptionFleschKincaidReadingGradeLevel': 11.045000000000002
           		},
           		'dataAccess': {
           			'dataAccessExists': True
           		},
           		'thumbnail': {
           			'thumbnailExists': True
           		},
           		'temporalBounding': {
           			'beginDescriptor': 'UNDEFINED',
           			'beginPrecision': None,
           			'beginIndexable': True,
           			'beginZoneSpecified': None,
           			'beginUtcDateTimeString': None,
           			'endDescriptor': 'UNDEFINED',
           			'endPrecision': None,
           			'endIndexable': True,
           			'endZoneSpecified': None,
           			'endUtcDateTimeString': None,
           			'instantDescriptor': 'UNDEFINED',
           			'instantPrecision': None,
           			'instantIndexable': True,
           			'instantZoneSpecified': None,
           			'instantUtcDateTimeString': None,
           			'rangeDescriptor': 'UNDEFINED'
           		},
           		'spatialBounding': {
           			'spatialBoundingExists': True,
           			'isValid': True,
           			'validationError': None
           		}
           	},
           	'fileInformation': None,
           	'fileLocations': {},
           	'publishing': {
           		'isPrivate': False,
           		'until': None
           	},
           	'relationships': [{
           		'type': 'COLLECTION',
           		'id': '075a3799-d02d-488b-b9de-a265e8905655'
           	}],
           	'errors': []
           }

    key = "3244b32e-83a6-4239-ba15-199344ea5d9"
    avsc_dir = os.path.dirname(os.path.realpath(__file__))
    key_schema = avro.load(os.path.join(avsc_dir, "primitive_string.avsc"))
    id, schema, version = sr.get_latest_schema(topic + "-value")
    print('Sending message for schema : ', id)
    while True:
        producer.produce(topic=topic, value=test, value_schema=schema, callback=lambda err, msg, obj=test: on_delivery(err, msg, obj))
        producer.poll(1)
