
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

    topic = "psi-granule-input-unknown"
    bootstrap_servers = "localhost:30886"
    schema_registry = "http://localhost:32234"

    base_conf = {
        'bootstrap.servers': bootstrap_servers,
        'schema.registry.url': schema_registry
         }

    producer = AvroProducer(base_conf)

    test = { "test" : "test" }

    key = "3244b32e-83a6-4239-ba15-199344ea5d9"
    avsc_dir = os.path.dirname(os.path.realpath(__file__))
    key_schema = avro.load(os.path.join(avsc_dir, "primitive_string.avsc"))
    id, schema, version = producer._serializer.registry_client.get_latest_schema(topic + "-value")
    print('Sending message for schema : ', id)
    while True:
        producer.produce(topic=topic, value=test, value_schema=schema, callback=lambda err, msg, obj=test: on_delivery(err, msg, obj))
        producer.poll(1)
