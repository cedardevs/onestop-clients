from producer.producer import produce


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

    key = "3244b32e-83a6-4239-ba15-199344ea5d9"
    test = {
        "type": "granule",
        "content": "",
        "contentType": "application/json",
        "method": "PUT",
        "source": "unknown",
        "operation": "ADD"
    }

    data = {key: test}

    produce(base_conf, topic, data)