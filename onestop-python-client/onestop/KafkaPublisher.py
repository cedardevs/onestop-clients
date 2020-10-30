import logging
from uuid import UUID
import json
import yaml

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.error import KafkaError
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer


class KafkaPublisher:
    conf = None

    def __init__(self, conf_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = self.get_logger("OneStop-Client", False)
        self.logger.info("Initializing " + self.__class__.__name__)
        self.metadata_type = self.conf['metadata_type']
        self.brokers = self.conf['brokers']
        self.schema_registry = self.conf['schema_registry']
        self.security = self.conf['security']['enabled']

        self.collection_topic = self.conf['collection_topic']
        self.granule_topic = self.conf['granule_topic']

        if self.metadata_type not in ['COLLECTION', 'GRANULE']:
            raise ValueError("metadata_type must be 'COLLECTION' or 'GRANULE'")

    def get_logger(self, log_name, create_file):

        # create logger
        log = logging.getLogger()

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.conf['log_level'] == "DEBUG":
            log.setLevel(level=logging.DEBUG)
        else:
            if self.conf['log_level'] == "INFO":
                log.setLevel(level=logging.INFO)
            else:
                log.setLevel(level=logging.ERROR)

        fh = None
        if create_file:
            # create file handler for logger.
            fh = logging.FileHandler(log_name)
            fh.setFormatter(formatter)

        # create console handler for logger.
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # add handlers to logger.
        if create_file:
            log.addHandler(fh)

        log.addHandler(ch)
        return log

    def connect(self):

        registry_client = self.register_client()
        metadata_producer = self.create_producer(registry_client)
        return metadata_producer

    def register_client(self):

        reg_conf = {'url': self.schema_registry}

        if self.security:
            reg_conf['ssl.ca.location'] = self.conf['security']['caLoc']
            reg_conf['ssl.key.location'] = self.conf['security']['keyLoc']
            reg_conf['ssl.certificate.location'] = self.conf['security']['certLoc']

        registry_client = SchemaRegistryClient(reg_conf)
        return registry_client

    def create_producer(self, registry_client):

        metadata_schema = None

        if self.metadata_type == "COLLECTION":
            metadata_schema = registry_client.get_latest_version(self.collection_topic + '-value').schema.schema_str

        if self.metadata_type == "GRANULE":
            metadata_schema = registry_client.get_latest_version(self.granule_topic + '-value').schema.schema_str

        metadata_serializer = AvroSerializer(metadata_schema, registry_client)
        producer_conf = {'bootstrap.servers': self.brokers}

        if self.security:
            producer_conf['security.protocol'] = 'SSL'
            producer_conf['ssl.ca.location'] = self.conf['security']['caLoc']
            producer_conf['ssl.key.location'] = self.conf['security']['keyLoc']
            producer_conf['ssl.certificate.location'] = self.conf['security']['certLoc']

        meta_producer_conf = producer_conf
        meta_producer_conf['value.serializer'] = metadata_serializer

        metadata_producer = SerializingProducer(meta_producer_conf)
        return metadata_producer

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            self.logger.error('Message delivery failed: {}'.format(err))
        else:
            self.logger.error('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publish_collection(self, collection_producer, collection_uuid, content_dict, method):
        self.logger.info('Publish collection')
        if type(collection_uuid) == bytes:
            key = str(UUID(bytes=collection_uuid))
        else:
            key = str(UUID(hex=collection_uuid))

        value_dict = {
            'type': 'collection',
            'content': json.dumps(content_dict),
            'contentType': 'application/json',
            'method': method,
            'source': 'unknown',
        }
        try:
            collection_producer.produce(topic=self.collection_topic, value=value_dict, key=key,
                                        on_delivery=self.delivery_report)
        except KafkaError:
            raise
        collection_producer.poll()

    def publish_granule(self, granule_producer, record_uuid, collection_uuid, content_dict, file_information,
                        file_locations):
        self.logger.info('Publish granule')
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
            granule_producer.produce(topic=self.granule_topic, value=value_dict, key=key,
                                     on_delivery=self.delivery_report)
        except KafkaError:
            raise
        granule_producer.poll()
