from confluent_kafka import Producer
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

import sys
import os


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.key()))

###
# topic name
# input_messages is a Dict of UUID(key) to message(value)
# config - values that you need to connect to kafka
###
def produceRawMessage(message):
    data_type = input("Enter type (granule or collection) : ")
    print(type)
    content_type = input("Enter MIME type associated with the value of the content field (json or xml) : ")
    print(content_type)
    method = input("Enter HTTP method used to send the input (PUT, PATCH, POST) : ")
    print(method)
    source = input("Enter the source of the input; for Granule: unknown, class, common-ingest, "
                   "for Collection: unknown or commet : ")
    print(source)
    operation = input("The specific operation to execute, mainly for PATCH-method input messages, "
                      "Use NO_OP for when the method is unambiguous on its own : ")
    print(operation)

    value = {
        "type": data_type,
        "content": message,
        "contentType": content_type,
        "method": method,
        "source": source,
        "operation": operation
    }

    return value


# def produceRawGranule(contentValue, contentType, method, source):
#
#     value = {
#         "type": "granule",
#         "content": contentValue,
#         "contentType": contentType,
#         "method": method,
#         "source": source,
#         "operation": "ADD"
#     }

#     # value
#     # input_message ={key, value}
#     # producer(topic, input_message)
#
# def produceRawCollection(contentValue, contentType, method, source):
#     value = {
#         "type": "collection",
#         "content": contentValue,
#         "contentType": contentType,
#         "method": method,
#         "source": source,
#         "operation": "ADD"
#     }


# def produceSendRawGranule(input_messages, contentType, method, source):
#
#     value = {
#         "type": "granule",
#         "content": contentValue,
#         "contentType": contentType,
#         "method": method,
#         "source": source,
#         "operation": "ADD"
#     }
#
#   produce and send granule mesage
#
# def produceSendRawCollection(input_messages, contentType, method, source):
#     value = {
#         "type": "collection",
#         "content": contentValue,
#         "contentType": contentType,
#         "method": method,
#         "source": source,
#         "operation": "ADD"
#     }
##   produce and send collection message

# def produceSpeci

def produce(topic, input_messages, config=None):
    producer_conf = {key: value.strip()
                     for key, value in config.items() if not key.startswith("schema.registry")}

    sr_conf = {key.replace("schema.registry.", ""): value.strip()
               for key, value in config.items() if key.startswith("schema.registry")}

    print(producer_conf)
    if 'bootstrap.servers' not in producer_conf:
        if 'KAFKA_BROKERS' in os.environ:
            kafka_brokers = os.environ['KAFKA_BROKERS'].split(',')

            producer_conf['bootstrap.servers'] = kafka_brokers

        else:
            raise ValueError(
                'Required bootstrap.servers not set. Pass bootstrap.servers or KAFKA_BROKERS environment variable not set')

    if 'url' not in sr_conf:
        if 'SCHEMA_REGISTRY_URL' in os.environ:
            schema_registry_url = os.environ['SCHEMA_REGISTRY_URL']
            sr_conf['url'] = schema_registry_url

        else:
            raise ValueError('Required schema.registry.url not set. SCHEMA_REGISTRY_URL environment variable not set')

    if topic is None:
        raise ValueError('Required topic field must be set')

    if len(input_messages) <= 0:
        raise ValueError('Required data field must not be empty.')

    producer = Producer(producer_conf)
    sr = CachedSchemaRegistryClient(sr_conf)
    ser = MessageSerializer(sr)

    # get schema
    id, schema, version = sr.get_latest_schema(topic + "-value")
    if schema:
        for key, value in input_messages.items():
            print('Sending message .... ')
            serializedMessage = ser.encode_record_with_schema(topic, schema, value)
            producer.produce(topic=topic, key=key, value=serializedMessage, callback=acked)
            # producer.flush() # bad idea, it limits throughput to the broker round trip time
            producer.poll(1)

    else:
        print('Schema not found for topic name: ', topic)
        sys.exit(1)
