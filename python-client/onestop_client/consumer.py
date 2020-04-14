from confluent_kafka import Consumer, KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

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
        except SerializerError as e:
            print("Message deserialization failed: {}".format(e))
            break
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        try:
            handler({
                'key': msg.key().decode('utf-8'),
                'value': ser.decode_message(msg.value(), is_key=False)
            })
        except e:
            print("Message handler failed: {}".format(e))
            break
    c.close()
