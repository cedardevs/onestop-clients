from producer.producer import produce, produceRawMessage
import uuid
import json

if __name__ == '__main__':

    topic = "psi-granule-input-unknown"
    # bootstrap_servers = "onestop-dev-cp-kafka:9092"
    bootstrap_servers = "localhost:9092"
    # schema_registry = "http://onestop-dev-cp-schema-registry:8081"
    schema_registry = "http://localhost:8081"

    base_conf = {
        'bootstrap.servers': bootstrap_servers,
        'schema.registry.url' : schema_registry
    }

    # generate a random uuid
    id = str(uuid.uuid4())
    key = id #"12398ad3-2acf-4125-98d4-0f3418677456"

    with open('sampleSqsPayload.json') as f:
        json_dict = json.loads(f.read())
        # print(json_dict['Message'])

    # extract content message from an sqs sample message
    content_value = json_dict['Message']

    value = {
        "type": "granule",
        "content": content_value,
        "contentType": "application/json",
        "method": "PUT",
        "source": "unknown",
        "operation": "ADD"
    }

    data = {key: value}

    # user input to produce a structure data
    # value = produceRawMessage(content_value)
    # print(value)

    produce(topic, data, base_conf)