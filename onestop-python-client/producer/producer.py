from confluent_kafka import Producer
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
from confluent_kafka.admin import AdminClient

import sys
import os
import re


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.key()))


def validate_uuid4(uuid_string):
    """
    Validate UUID string is in fact a valid uuid4.

    Parameters
    ----------
        uuid_string : str
            uuid as a string
    """
    # prevent UUIDs with uppercase A-F to align strictly with spec in our incoming string representations of IDs
    regex = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
    match = regex.match(uuid_string)
    return bool(match)


def producer_config(config=None):
    """
        Config values for kafka brokers and schema registry

    Parameters
    ----------
        config: dict
            the config values that needed by the produce
        sample config
        -------------
        sample_config = {
            'bootstrap.servers': bootstrap_servers,
            'schema.registry.url' : schema_registry
         }

     """
    if config is not None:
        producer_conf = {key: value.strip()
                         for key, value in config.items() if not key.startswith("schema.registry")}

        sr_conf = {key.replace("schema.registry.", ""): value.strip()
                   for key, value in config.items() if key.startswith("schema.registry")}

    if producer_conf is None or 'bootstrap.servers' not in producer_conf:
        if 'KAFKA_BROKERS' in os.environ:
            kafka_brokers = os.environ['KAFKA_BROKERS'].split(',')

            producer_conf['bootstrap.servers'] = kafka_brokers

        else:
            raise ValueError(
                'Required bootstrap.servers not set. Pass bootstrap.servers or KAFKA_BROKERS environment variable not set')

    if sr_conf is None or 'url' not in sr_conf:
        if 'SCHEMA_REGISTRY_URL' in os.environ:
            schema_registry_url = os.environ['SCHEMA_REGISTRY_URL']
            sr_conf['url'] = schema_registry_url

        else:
            raise ValueError('Required schema.registry.url not set. SCHEMA_REGISTRY_URL environment variable not set')

    return producer_conf, sr_conf


def produce(topic, input_messages, config=None):
    """
        produce initiate sending a message to Kafka, call the produce method passing in the input_messages key/value
        and and callback
    Parameters
    ----------
        topic: str
            topic where the input message publish too
        input_messages: dict
            a key/value input messages
        config: dict
            the config values that needed by the produce

     """
    if topic is None:
        raise ValueError('Required topic field must be set')

    if len(input_messages) <= 0:
        raise ValueError('Required data field must not be empty.')

    bootstrap_servers, schema_registry = producer_config(config)
    producer = Producer(bootstrap_servers)
    sr = CachedSchemaRegistryClient(schema_registry)
    ser = MessageSerializer(sr)

    # get schema
    id, schema, version = sr.get_latest_schema(topic + "-value")
    if schema:
        for key, value in input_messages.items():
            if validate_uuid4(key):
                print('Sending message .... ')
                serializedMessage = ser.encode_record_with_schema(topic, schema, value)
                producer.produce(topic=topic, key=key, value=serializedMessage, callback=acked)
                # producer.flush() # bad idea, it limits throughput to the broker round trip time
                producer.poll(1)
            else:
                print('Invalid UUID String: ', key)

    else:
        print('Schema not found for topic name: ', topic)
        sys.exit(1)


def produce_and_publish_raw_granule(topic, key, value, method, config=None):
    value = {
        "type": "granule",
        "content": value,
        "contentType": "application/json",
        "method": method,
        "source": "unknown",
        "operation": "NO_OP"
    }

    data = {key: value}

    produce(topic, data, config)


def produce_and_publish_raw_collection(topic, key, value, method, config=None):
    value = {
        "type": "collection",
        "content": value,
        "contentType": "application/xml",
        "method": method,
        "source": "unknown",
        "operation": "NO_OP"
    }

    data = {key: value}

    produce(topic, data, config)


def produce_raw_message(message):
    """
        Uses user's inputs to construct a structured input value
    Parameters
    ----------
        message: json str
            The raw input content as a string

    User input Parameters
    ---------------------
        data_type: str
            The type of record represented by this input (must be either granule or collection)
        content_type: str
            MIME type associated with the value of the content field (must be either json or xml)
        method: str
            Enter HTTP method used to send the input (PUT, PATCH, POST)
        source: str
            Enter the source of the input;
                Granule: unknown, class, common-ingest
                Collection: unknown or commet
        operation:  str
            The specific operation to execute,
            NOTE: mainly for PATCH-method input messages Use NO_OP for when the method is unambiguous on its own
    """
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


def list_topics(conf):
    kadmin = AdminClient(conf)
    md = kadmin.list_topics(timeout=10)

    print(" {} topics:".format(len(md.topics)))
    for t in iter(md.topics.values()):
        if t.error is not None:
            errstr = ": {}".format(t.error)
        else:
            errstr = ""
# todo list by granule and collection
        print("  \"{}\" {}".format(t, errstr))
    # return kadmin.list_topics().topics

