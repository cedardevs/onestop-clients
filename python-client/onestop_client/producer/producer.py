
from kafka import KafkaProducer
# from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
# from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

import json

#TODO: 1. serialize using avro
#      2. use config values for topic name

class Producer(object):
    def __init__(self, kafka_brokers):
        self.producer = KafkaProducer(
            value_serializer=lambda v: json.dumps(v).encode('utf-8'), #replace by avro
            bootstrap_servers=kafka_brokers
        )
    def sendSqsToKafka(self, json_data):
        self.producer.send('topic-name', json_data) # topic env var and avro message