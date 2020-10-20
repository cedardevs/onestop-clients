from onestop.producer import produce, list_topics, produce_and_publish_raw_granule, produce_and_publish_raw_collection
import json
import uuid

if __name__ == '__main__':

    topic = "psi-granule-input-unknown"
    # bootstrap_servers = "onestop-dev-cp-kafka:9092"
    bootstrap_servers = "localhost:9092"
    # schema_registry = "http://onestop-dev-cp-schema-registry:8081"
    schema_registry = "http://localhost:8081"

    base_conf = {
        'bootstrap.servers': bootstrap_servers,
        'schema.registry.url': schema_registry
    }

    with open('./sampleSqsPayload.json') as f:
        json_dict = json.loads(f.read())
        # print(json_dict['Message'])
    # extract content message from an sqs sample message
    content_value = json_dict['Message']
    fileId = json.loads(content_value)['discovery']['fileIdentifier']

    value = {
        "type": "granule",
        "content": str(content_value),
        "contentType": "application/json",
        "method": "PUT",
        "source": "unknown",
        "operation": "ADD"
    }
    # publish bulk messages
    data = {}
    for x in range(10):
        # generate a random uuid
        key = str(uuid.uuid4())
        data[key] = value

    # publish a single data
    # data = {fileId: value}

    #list topoc
    list_topics({'bootstrap.servers': bootstrap_servers})

    # user input to produce a structure data
    # value = produceRawMessage(content_value)

    print("publish messages using generic producer ...")
    produce(topic, data, base_conf)

    # #def produce_and_publish_raw_collection(topic, key, value, method, config=None):
    print("publish messages using produce_and_publish_raw_collection ...")
    produce_and_publish_raw_collection("psi-collection-input-unknown", fileId, content_value, "PUT", base_conf)

    print("publish messages using produce_and_publish_raw_granule ...")
    produce_and_publish_raw_granule("psi-granule-input-unknown", fileId, content_value, "PUT", base_conf)

