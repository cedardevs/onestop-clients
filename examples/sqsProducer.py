from onestop_client.producer import produce


if __name__ == '__main__':

    topic = "psi-granule-input-unknown"
    bootstrap_servers = "onestop-dev-cp-kafka:9092"
    schema_registry = "http://onestop-dev-cp-schema-registry:8081"

    base_conf = {
        'bootstrap.servers': bootstrap_servers,
        'schema.registry.url' : schema_registry
    }

    key = "12398ad3-2acf-4125-98d4-0f3418677123"
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