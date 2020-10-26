from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.error import KafkaError
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer

from uuid import UUID
import json
import yaml


class KafkaPublisher:
    conf = None

    def __init__(self, confLoc):

        with open(confLoc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)
            print(str(self.conf))

        self.brokers = self.conf['brokers']
        self.schema_registry = self.conf['schema_registry']
        self.security = self.conf['security']['enabled']

        self.collection_topic = self.conf['collection_topic']
        self.granule_topic = self.conf['granule_topic']

    def connect(self):
        registry_client = self.register_client()
        self.create_producers(registry_client)

    def register_client(self):

        reg_conf = {'url': self.schema_registry}

        if self.security:
            reg_conf['ssl.ca.location'] = self.conf['security']['caLoc']
            reg_conf['ssl.key.location'] = self.conf['security']['keyLoc']
            reg_conf['ssl.certificate.location'] = self.conf['security']['certLoc']

        registry_client = SchemaRegistryClient(reg_conf)
        return registry_client

    def create_producers(self, registry_client):

        self.collectionSchema = registry_client.get_latest_version(self.collection_topic+'-value').schema.schema_str
        self.granuleSchema = registry_client.get_latest_version(self.granule_topic+'-value').schema.schema_str

        self.collection_serializer = AvroSerializer(self.collectionSchema, registry_client)
        self.granule_serializer = AvroSerializer(self.granuleSchema, registry_client)

        producer_conf = {'bootstrap.servers': self.brokers}

        if self.security:
            producer_conf['security.protocol'] = 'SSL'
            producer_conf['ssl.ca.location'] = self.conf['security']['caLoc']
            producer_conf['ssl.key.location'] = self.conf['security']['keyLoc']
            producer_conf['ssl.certificate.location'] = self.conf['security']['certLoc']

        col_producer_conf = producer_conf
        col_producer_conf['value.serializer'] = self.collection_serializer

        grn_producer_conf = producer_conf
        grn_producer_conf['value.serializer'] = self.granule_serializer

        self.collection_producer = SerializingProducer(col_producer_conf)
        self.granule_producer = SerializingProducer(grn_producer_conf)

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def flush(self, type):
        if type not in ['collection', 'granule']:
            raise ValueError("type must be 'collection' or 'granule'")
        if type == 'collection':
            self.collection_producer.flush()
        elif type == 'granule':
            self.granule_producer.flush()

    def publish_collection(self, collection_uuid, content_dict):
        print('publish collection')
        if type(collection_uuid) == bytes:
            key = str(UUID(bytes=collection_uuid))
        else:
            key = str(UUID(hex=collection_uuid))

        value_dict = {
            'type': 'collection',
            'content': json.dumps(content_dict),
            'contentType': 'application/json',
            'method': 'PUT',
            'source': 'unknown',
        }
        try:
            self.collection_producer.produce(topic=self.collection_topic, value=value_dict, key=key,
                                             on_delivery=self.delivery_report)
        except KafkaError:
            raise
        self.collection_producer.poll()

    def publish_record(self, record_uuid, collection_uuid, content_dict, file_information, file_locations):
        print('publish record')
        if type(record_uuid) == bytes:
            key = str(UUID(bytes=collection_uuid))
        else:
            key = str(UUID(hex=collection_uuid))
        if type(collection_uuid) == bytes:
            content_dict['relationships'] = [{"type": "COLLECTION", "id": collection_uuid.hex()}]
        else:
            content_dict['relationships'] = [{"type": "COLLECTION", "id": str(collection_uuid)}]

        content_dict['fileInformation'] = file_information
        content_dict['fileLocations'] = file_locations

        value_dict = {
            'type': 'granule',
            'content': json.dumps(content_dict),
            'method': 'PUT',
            'source': 'unknown',
            'operation': None,
            'relationships': [{'type': 'COLLECTION', 'id': collection_uuid}]
        }
        try:
            self.granule_producer.produce(topic=self.granule_topic, value=value_dict, key=key,
                                          on_delivery=self.delivery_report)
        except KafkaError:
            raise
        self.granule_producer.poll()
