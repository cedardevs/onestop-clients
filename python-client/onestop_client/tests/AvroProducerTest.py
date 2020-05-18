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

def error_cb(err):
    print('Error: %s' % err)

if __name__ == '__main__':

    topic = "psi-granule-input-unknown"
    bootstrap_servers = "onestop-dev-cp-kafka:9092"
    schema_registry = "http://onestop-dev-cp-schema-registry:8081"

    base_conf = {
        'bootstrap.servers': bootstrap_servers,
        'error_cb': error_cb
         }

    producer = Producer(base_conf)

    test = {
        "type": "granule",
        "content": "",
        "contentType": "application/json",
        "method": "PUT",
        "source": "unknown",
        "operation": "ADD"
    }

    sr_conf = {'url': schema_registry}

    sr = CachedSchemaRegistryClient(sr_conf)
    ser = MessageSerializer(sr)

    key = "3244b32e-83a6-4239-ba15-199344ea5d9"
    id, schema, version = sr.get_latest_schema(topic + "-value")
    print('Sending message for schema : ', id)
    serializedMessage = ser.encode_record_with_schema(topic, schema, test)

    producer.produce(topic=topic, key=key, value=serializedMessage, callback=lambda err, msg, obj=test: on_delivery(err, msg, obj))
    producer.poll(1)
    producer.flush()