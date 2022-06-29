import json

from uuid import UUID
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.error import KafkaError
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
from onestop.util.ClientLogger import ClientLogger

class KafkaPublisher:
    """
    A class to publish to kafka topics

    Attributes
    ----------
        metadata_type: str
            type of metadata (COLLECTION or GRANULE)
        brokers: str
            brokers (kubernetes service)
        schema_registry: str
            schema registry (kubernetes service)
        security_enabled: boolean
            defines if security is in place
        security_caLoc: str
            Kafka schema registry certification authority (CA) file location.
        security_keyLoc: str
            Kafka schema registry client's private key file location.
        security_certLoc: str
            Kafka schema registry client's public key file location.
        collection_topic: str
            collection topic you want to produce to
        granule_topic: str
            granule topic you want to produce to
        logger: Logger object
                utilizes python logger library and creates logging for our specific needs

    Methods
    -------
        register_client()
            registers to schema registry client based on configs

        create_producer(registry_client)
            creates a SerializingProducer object to produce to kafka topic

        connect()
            utilizes register_client() and create_producer(registry_client) to connect to schema registry and allow for producing to kafka topics

        publish_collection(collection_producer, collection_uuid, content_dict, method)
            Publish collection to collection topic

        publish_granule(granule_producer, collection_uuid, content_dict)
            Publish granule to granule topic
    """

    def __init__(self, kafka_publisher_metadata_type, brokers, schema_registry, security, collection_topic_publish, granule_topic_publish, log_level='INFO', **wildargs):
        """
        Attributes
        ----------
            kafka_publisher_metadata_type: str
                type of metadata (COLLECTION or GRANULE)
            brokers: str
                brokers (kubernetes service)
            group_id: str
                Client group id string. All clients sharing the same group.id belong to the same group
            auto_offset_reset: str
                Action to take when there is no initial offset in offset store or the desired offset is out of range (smallest, earliest, beginning, largest, latest, end, error)
            schema_registry: str
                schema registry (kubernetes service) URL
            security: dict
                enabled boolean: Whether to use security for kafka schema registry client.
                caLoc str: Kafka schema registry certification authority (CA) file location.
                keyLoc str: Kafka schema registry client's private key file location.
                certLoc str: Kafka schema registry client's public key file location.

            collection_topic: str
                collection topic you want to produce to
            granule_topic: str
                granule topic you want to produce to
        """
        self.metadata_type = kafka_publisher_metadata_type.upper()
        self.brokers = brokers
        self.schema_registry = schema_registry
        self.security_enabled = security['enabled']

        if self.security_enabled:
            self.security_caLoc = security['caLoc']
            self.security_keyLoc = security['keyLoc']
            self.security_certLoc = security['certLoc']

        self.collection_topic = collection_topic_publish
        self.granule_topic = granule_topic_publish

        if self.metadata_type not in ['COLLECTION', 'GRANULE']:
            raise ValueError("metadata_type of '%s' must be 'COLLECTION' or 'GRANULE'"%(self.metadata_type))

        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
        self.logger.info("Initializing " + self.__class__.__name__)

        if wildargs:
            self.logger.debug("Superfluous parameters in constructor call: " + str(wildargs))

    def connect(self):
        """
        Utilizes register_client() and create_producer(registry_client) to connect to schema registry and allow for producing to kafka topics

        :return: SerializingProducer Object
            based on initial constructor values
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

        if self.security_enabled:
            reg_conf['ssl.ca.location'] = self.security_caLoc
            reg_conf['ssl.key.location'] = self.security_keyLoc
            reg_conf['ssl.certificate.location'] = self.security_certLoc

        registry_client = SchemaRegistryClient(reg_conf)
        return registry_client

    def create_producer(self, registry_client):
        """
        Creates a SerializingProducer object to produce to kafka topic

        :param registry_client: SchemaRegistryClient
            get this from register_client()

        :return: SerializingProducer Object
            based on initial constructor values
        """
        topic = None

        if self.metadata_type == "COLLECTION":
            topic = self.collection_topic

        if self.metadata_type == "GRANULE":
            topic = self.granule_topic
        self.logger.debug("topic: "+str(topic))

        metadata_schema = registry_client.get_latest_version(topic + '-value').schema.schema_str
        self.logger.debug("metadata_schema: "+metadata_schema)

        metadata_serializer = AvroSerializer(schema_str=metadata_schema, schema_registry_client=registry_client)
        conf = {
            'bootstrap.servers': self.brokers,
            'value.serializer': metadata_serializer}

        if self.security_enabled:
            conf['security.protocol'] = 'SSL'
            conf['ssl.ca.location'] = self.security_caLoc
            conf['ssl.key.location'] = self.security_keyLoc
            conf['ssl.certificate.location'] = self.security_certLoc

        self.logger.debug("Serializing conf: "+str(conf))
        metadata_producer = SerializingProducer(conf)
        return metadata_producer

    def delivery_report(self, err, msg):
        """
        Called once for each message produced to indicate delivery of message. Triggered by poll() or flush().

        :param err: str
            err produced after publishing, if there is one
        :param msg: dict
            the message that was published to topic
        """
        if err is not None:
            self.logger.error('Message delivery failed: {}'.format(err))
        else:
            self.logger.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    @staticmethod
    def get_collection_key_from_uuid(collection_uuid):
        """
        Create a key to use in a kafka message from the given string representation of the collection UUID.
        :param collection_uuid: str
            collection string to turn into a key.
        :return:
        """
        if type(collection_uuid) == bytes:
            return str(UUID(bytes=collection_uuid))
        else:
            return str(UUID(hex=collection_uuid))

    def publish_collection(self, collection_producer, collection_uuid, content_dict, method):
        """
        Publish a collection to the collection topic

        :param collection_producer: SerializingProducer
            use connect()
        :param collection_uuid: str
            collection uuid that you want the collection to have
        :param content_dict: dict
            dictionary containing information you want to publish
        :param method: str
            POST/PUT

        :return: str
            returns msg if publish is successful, kafka error if it wasn't successful
        """
        self.logger.info('Publishing collection')

        key = self.get_collection_key_from_uuid(collection_uuid)

        value_dict = {
            'type': 'collection',
            'content': json.dumps(content_dict),
            'contentType': 'application/json',
            'method': method,
            'source': 'unknown',
        }
        self.logger.debug('Publishing collection with topic='+self.collection_topic+' key='+key+' value='+str(value_dict))
        collection_producer.produce(
            topic=self.collection_topic,
            value=value_dict,
            key=key,
            on_delivery=self.delivery_report)
        collection_producer.poll()

    def publish_granule(self, granule_producer, collection_uuid, content_dict):
        """
        Publish a granule to the granule topic

        :param granule_producer: SerializingProducer
            use connect()
        :param collection_uuid: str
            collection uuid associated with the granule
        :param content_dict: dict
            information you want to publish

        :return: str
            returns msg if publish is successful, kafka error if it wasn't successful
        """
        self.logger.info('Publish granule')

        key = self.get_collection_key_from_uuid(collection_uuid)

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

        self.logger.debug('Publishing granule with topic='+self.granule_topic+' key='+key+' value='+str(value_dict))
        granule_producer.produce(
            topic=self.granule_topic,
            value=value_dict,
            key=key,
            on_delivery=self.delivery_report)

        granule_producer.poll()
