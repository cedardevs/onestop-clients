import logging
import yaml

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.error import KafkaError
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

class KafkaConsumer:
    """
    A class used to consume messages from Kafka

    Attributes
    ----------
    conf: yaml file
        kafka-publisher-config-dev.yml
    logger: Logger object
            utilizes python logger library and creates logging for our specific needs
    logger.info: Logger object
        logging statement that occurs when the class is instantiated
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

    create_consumer(registry_client)
        subscribes to topic defined in configs and creates a consumer to deserialize messages from topic

    connect()
        utilizes register_client() and create_consumer(registry_client) to connect to schema registry and allow for consumption of topics

    consume(metadata_consumer, handler)
        asynchronously polls for messages in the connected topic, results vary depending on the handler function that is passed into it
    """
    conf = None

    def __init__(self, conf_loc):
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = self.get_logger(self.__class__.__name__, False)
        self.logger.info("Initializing " + self.__class__.__name__)
        self.metadata_type = self.conf['metadata_type']
        self.brokers = self.conf['brokers']
        self.group_id = self.conf['group_id']
        self.auto_offset_reset = self.conf['auto_offset_reset']
        self.schema_registry = self.conf['schema_registry']
        self.security = self.conf['security']['enabled']

        self.collection_topic = self.conf['collection_topic_consume']
        self.granule_topic = self.conf['granule_topic_consume']

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

        if self.security:
            consumer_conf['security.protocol'] = 'SSL'
            consumer_conf['ssl.ca.location'] = self.conf['security']['caLoc']
            consumer_conf['ssl.key.location'] = self.conf['security']['keyLoc']
            consumer_conf['ssl.certificate.location'] = self.conf['security']['certLoc']

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
