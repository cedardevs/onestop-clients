import logging
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger()

def consume(config, topic, handler):
    """
    Starts a consumer and calls the given handler for each consumed message.
    Assumes that keys are serialized as strings and values are serialized
    as Avro objects with their schemas stored in a Confluent Schema Registry.
    """
    c_conf = {}
    for key, value in config.items(): 
        if not key.startswith("schema.registry"):
           if not value is None:
               c_conf[key] = value.strip()

    if "auto.offset.reset" in c_conf:
        print("offset provided")
    else:
        c_conf['auto.offset.reset'] = 'earliest'
    
    if "group.id" in c_conf:
        print("group id provided")
    else:
        c_conf['group.id'] = 'sme_test'

    c = Consumer(c_conf)

    c.subscribe([topic])

    sr_conf = {key.replace("schema.registry.", ""): value.strip()
                for key, value in config.items() if key.startswith("schema.registry")}
    
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
