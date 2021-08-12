import logging
from uuid import UUID
import json
import yaml

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.error import KafkaError
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer


class KafkaPublisher:
    """
    A class to publish to kafka topics

    Attributes
    ----------
    conf: yaml file
        config/kafka-publisher-config-dev.yml
    logger: Logger object
            utilizes python logger library and creates logging for our specific needs
    logger.info: Logger object
        logging statement that occurs when the class is instantiated
    metadata_type: str
        type of metadata (COLLECTION or GRANULE)
    brokers: str
        brokers (kubernetes service)
    schema_registry: str
        schema registry (kubernetes service)
    security: boolean
        defines if security is in place
    collection_topic: str
        collection topic you want to consume
    granule_topic: str
        granule topic you want to consume

    Methods
    -------
    get_logger(log_name, create_file)
        creates logger file

    register_client()
        registers to schema registry client based on configs

    create_producer(registry_client)
        creates a SerializingProducer object to produce to kafka topic

    connect()
        utilizes register_client() and create_producer(registry_client) to connect to schema registry and allow for producing to kafka topics

    publish_collection(collection_producer, collection_uuid, content_dict, method)
        Publish collection to collection topic

    publish_granule(granule_producer, record_uuid, collection_uuid, content_dict)
        Publish granule to granule topic
    """
    conf = None

    def __init__(self, conf_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = self.get_logger(self.__class__.__name__, False)
        self.logger.info("Initializing " + self.__class__.__name__)
        self.metadata_type = self.conf['metadata_type']
        self.brokers = self.conf['brokers']
        self.schema_registry = self.conf['schema_registry']
        self.security = self.conf['security']['enabled']

        self.collection_topic = self.conf['collection_topic_produce']
        self.granule_topic = self.conf['granule_topic_produce']

        if self.metadata_type not in ['COLLECTION', 'GRANULE']:
            raise ValueError("metadata_type must be 'COLLECTION' or 'GRANULE'")

    def get_logger(self, log_name, create_file):
        """
        Utilizes python logger library and creates logging

        :param log_name: str
            name of log to be created
        :param create_file: boolean
            defines whether of not you want a logger file to be created

        :return: Logger object
        """

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
        """
        Utilizes register_client() and create_producer(registry_client) to connect to schema registry and allow for producing to kafka topics

        :return: SerializingProducer Object
            based on config values
        """
        registry_client = self.register_client()
        metadata_producer = self.create_producer(registry_client)
        return metadata_producer

    def register_client(self):
        """
        Registers to schema registry client based on configs

        :return: SchemaRegistryClient (confluent kafka library)
        """

        reg_conf = {'url': self.schema_registry}

        if self.security:
            reg_conf['ssl.ca.location'] = self.conf['security']['caLoc']
            reg_conf['ssl.key.location'] = self.conf['security']['keyLoc']
            reg_conf['ssl.certificate.location'] = self.conf['security']['certLoc']

        registry_client = SchemaRegistryClient(reg_conf)
        return registry_client

    def create_producer(self, registry_client):
        """
        Creates a SerializingProducer object to produce to kafka topic

        :param registry_client: SchemaRegistryClient
            get this from register_client()

        :return: SerializingProducer Object
            based on config values
        """
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
        """
        Called once for each message produced to indicate delivery result. Triggered by poll() or flush().

        :param err: str
            err produced after publishing, if there is one
        :param msg: dict
            the message that was published to topic
        """
        if err is not None:
            self.logger.error('Message delivery failed: {}'.format(err))
        else:
            self.logger.error('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publish_collection(self, collection_producer, collection_uuid, content_dict, method):
        """
        Publish collection to collection topic

        :param collection_producer: SerializingProducer
            use connect()
        :param collection_uuid: str
            collection uuid that you want colelction to have
        :param content_dict: dict
            dictionary containing information you want to publish
        :param method: str
            POST/PUT

        :return: str
            returns msg if publish is successful, kafka error if it wasn't successful
        """
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

    def publish_granule(self, granule_producer, record_uuid, collection_uuid, content_dict):
        """
        Publishes granule to granule topic

        :param granule_producer: SerializingProducer
            use connect()
        :param record_uuid: str
            record uuid associated with the granule
        :param collection_uuid: str
            collection uuid associated with the granule
        :param content_dict: dict
            information you want to publish

        :return: str
            returns msg if publish is successful, kafka error if it wasn't successful
        """
        self.logger.info('Publish granule')

        if type(record_uuid) == bytes:
            key = str(UUID(bytes=collection_uuid))
        else:
            key = str(UUID(hex=collection_uuid))
        """
        if type(collection_uuid) == bytes:
            content_dict['relationships'] = [{"type": "COLLECTION", "id": collection_uuid.hex()}]
        else:
            content_dict['relationships'] = [{"type": "COLLECTION", "id": str(collection_uuid)}]

        content_dict['fileInformation'] = file_information
        content_dict['fileLocations'] = file_locations
        """

        """
                    'relationships': content_dict['relationships'],
                    'discovery': content_dict['discovery'],
                    'fileInformation': content_dict['fileInformation']
                    """

        value_dict = {
            'type': 'granule',
            'content': json.dumps(content_dict),
            #'contentType': 'application/json',
            'method': 'PUT',
            'source': 'unknown',
            'operation': None,
            'relationships': content_dict['relationships'],
            'errors': content_dict['errors'],
            'analysis': content_dict['analysis'],
            'fileLocations': {'fileLocation': content_dict['fileLocations']},
            'fileInformation': content_dict['fileInformation'],
            'discovery': content_dict['discovery']
        }

        try:
            granule_producer.produce(topic=self.granule_topic, value=value_dict, key=key,
                                     on_delivery=self.delivery_report)
        except KafkaError:
            raise
        granule_producer.poll()
