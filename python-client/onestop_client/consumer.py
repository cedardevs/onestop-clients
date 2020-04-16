import logging
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger()

def consume(config, topics, handler):
    """
    Starts a consumer and calls the given handler for each consumed message.
    Assumes that keys are serialized as strings and values are serialized
    as Avro objects with their schemas stored in a Confluent Schema Registry.
    """
    c_conf = {key: value.strip()
                for key, value in config.items() if not key.startswith("schema.registry")}

    print(c_conf)

    c = Consumer(c_conf)
    for topic in topics:
        topic = topic.strip()
        print(topic)

    c.subscribe(topics)

    sr_conf = {key.replace("schema.registry.", ""): value.strip()
                for key, value in config.items() if key.startswith("schema.registry")}

    print(sr_conf)

    sr = CachedSchemaRegistryClient(sr_conf)
    ser = MessageSerializer(sr)

    while True:
        try:
            msg = c.poll(10)
            if msg is None:
                continue
            if msg.error():
                log.error("Consumer error: {}".format(msg.error()))
                continue
            key = msg.key().decode('utf-8')
            value = ser.decode_message(msg.value(), is_key=False)
        except Exception as e:
            log.error("Message consumption failed: {}".format(e))
            break
        try:
            handler(key, value)
        except Exception as e:
            log.error("Message handler failed: {}".format(e))
            break
    c.close()
