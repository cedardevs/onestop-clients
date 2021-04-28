from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.error import KafkaError
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from onestop.util.ClientLogger import ClientLogger

class KafkaConsumer:
    """
    A class used to consume messages from Kafka

    Attributes
    ----------
        metadata_type: str
            type of metadata (COLLECTION or GRANULE)
        brokers: str
            brokers (kubernetes service)
        group_id: str
            Client group id string. All clients sharing the same group.id belong to the same group
        auto_offset_reset: str
            Action to take when there is no initial offset in offset store or the desired offset is out of range (smallest, earliest, beginning, largest, latest, end, error)
        schema_registry: str
            schema registry (kubernetes service)
        security_enabled: boolean
            Whether to use security for the kafka schema registry client.
        security_caLoc: str
            Kafka schema registry certification authority (CA) file location.
        security_keyLoc: str
            Kafka schema registry client's private key file location.
        security_certLoc: str
            Kafka schema registry client's public key file location.
        collection_topic_consume: str
            collection topic you want to consume
        granule_topic_consume: str
            granule topic you want to consume
        logger: Logger object
                utilizes python logger library and creates logging for our specific needs

    Methods
    -------
        register_client()
            registers to schema registry client based on configs

        connect()
            utilizes register_client() and create_consumer(registry_client) to connect to schema registry and allow for consumption of topics

        create_consumer(registry_client)
            subscribes to topic defined in configs and creates a consumer to deserialize messages from topic

        consume(metadata_consumer, handler)
            asynchronously polls for messages in the connected topic, results vary depending on the handler function that is passed into it
    """

    def __init__(self, metadata_type, brokers, group_id, auto_offset_reset, schema_registry, security, collection_topic_consume, granule_topic_consume, log_level = 'INFO', **wildargs):
        """
        Attributes
        ----------
            metadata_type: str
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

            collection_topic_consume: str
                collection topic you want to consume
            granule_topic_consume: str
                granule topic you want to consume
            log_level: str
                    What log level to use for this class
        """

        self.metadata_type = metadata_type
        self.brokers = brokers
        self.group_id = group_id
        self.auto_offset_reset = auto_offset_reset
        self.schema_registry = schema_registry
        self.security_enabled = security['enabled']

        if self.security_enabled:
            self.security_caLoc = security['caLoc']
            self.security_keyLoc = security['keyLoc']
            self.security_certLoc = security['certLoc']

        self.collection_topic_consume = collection_topic_consume
        self.granule_topic_consume = granule_topic_consume

        if self.metadata_type not in ['COLLECTION', 'GRANULE']:
            raise ValueError("metadata_type must be 'COLLECTION' or 'GRANULE'")

        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
        self.logger.info("Initializing " + self.__class__.__name__)

        if wildargs:
            self.logger.error("There were extra constructor arguments: " + str(wildargs))

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

    def connect(self):
        """
        Utilizes register_client() and create_consumer(registry_client) to connect to schema registry and allow for consumption of topics

        :return: DeserializingConsumer object
        """
        registry_client = self.register_client()
        metadata_consumer = self.create_consumer(registry_client)
        return metadata_consumer

    def create_consumer(self, registry_client):
        """
        Subscribes to topic defined in configs and creates a consumer to deserialize messages from topic

        :param registry_client: SchemaRegistryClient object
            get this from register_client()

        :return: DeserializingConsumer object
        """
        metadata_schema = None
        topic = None
        if self.metadata_type == "COLLECTION":
            metadata_schema = registry_client.get_latest_version(self.collection_topic + '-value').schema.schema_str
            topic = self.collection_topic

        if self.metadata_type == "GRANULE":
            metadata_schema = registry_client.get_latest_version(self.granule_topic + '-value').schema.schema_str
            topic = self.granule_topic

        metadata_deserializer = AvroDeserializer(metadata_schema, registry_client)

        consumer_conf = {'bootstrap.servers': self.brokers}

        if self.security_enabled:
            consumer_conf['security.protocol'] = 'SSL'
            consumer_conf['ssl.ca.location'] = self.security_caLoc
            consumer_conf['ssl.key.location'] = self.security_keyLoc
            consumer_conf['ssl.certificate.location'] = self.security_certLoc

        meta_consumer_conf = consumer_conf
        meta_consumer_conf['key.deserializer'] = StringDeserializer('utf-8')
        meta_consumer_conf['value.deserializer'] = metadata_deserializer
        meta_consumer_conf['group.id'] = self.group_id
        meta_consumer_conf['auto.offset.reset'] = self.auto_offset_reset

        metadata_consumer = DeserializingConsumer(meta_consumer_conf)
        metadata_consumer.subscribe([topic])
        return metadata_consumer

    def consume(self, metadata_consumer, handler):
        """
        Asynchronously polls for messages in the connected topic, results vary depending on the handler function that is passed into it

        :param metadata_consumer: Deserializing Consumer object
            use the connect() function to get this
        :param handler: callback function
            response of consume depends on handler passed in

        :return: dependent on handler
        """
        self.logger.info('Consuming from topic')
        while True:
            try:
                msg = metadata_consumer.poll(10)

                if msg is None:
                    print('No Messages')
                    continue

                key = msg.key()
                value = msg.value()


            except KafkaError:
                raise
            try:
                handler(key, value)
            except Exception as e:
                self.logger.error("Message handler failed: {}".format(e))
                break
        metadata_consumer.close()
