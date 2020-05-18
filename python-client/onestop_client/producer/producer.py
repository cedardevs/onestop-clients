from confluent_kafka import Producer
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
        print('Message {} delivery failed for user {} with error {}')
    else:
        print('Message {} successfully produced to {} [{}] at offset {}')


def produce(config, topic, data):

    producer_conf = {key: value.strip()
        for key, value in config.items() if not key.startswith("schema.registry")}

    sr_conf = {key.replace("schema.registry.", ""): value.strip()
                for key, value in config.items() if key.startswith("schema.registry")}

    print(producer_conf)
    if 'bootstrap.servers' not in producer_conf:
        if 'KAFKA_BROKERS' in os.environ:
            kafka_brokers = os.environ['KAFKA_BROKERS'].split(',')
        else:
            raise ValueError('Required bootstrap.servers not set. Pass bootstrap.servers or KAFKA_BROKERS environment variable not set')

    if 'url' not in sr_conf:
        if 'SCHEMA_REGISTRY_URL' in os.environ:
            schema_registry_url = os.environ['SCHEMA_REGISTRY_URL']
        else:
            raise ValueError('Required schema.registry.url not set. SCHEMA_REGISTRY_URL environment variable not set')

    if topic is None:
        raise ValueError('Required topic field must be set')

    if len(data) <= 0:
        raise ValueError('Required data field must not be empty.')

    producer = Producer(producer_conf)
    sr = CachedSchemaRegistryClient(sr_conf)
    ser = MessageSerializer(sr)

    key = '8c223821-c4ee-4d3d-b1a6-7506a67a9cf0'
    id, schema, version = sr.get_latest_schema(topic + "-value")
    print('Sending message for schema : ', id)
    print(schema.name)
    
    for key, value in data.items():
        serializedMessage = ser.encode_record_with_schema(topic, schema, data)
        producer.produce(topic=topic, key=key, value=serializedMessage)
        producer.flush()