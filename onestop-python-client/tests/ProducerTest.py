import unittest
import json

from producer import produce

class TestSQSHandler():
    topic = "psi-granule-input-unknown"
    # bootstrap_servers = "onestop-dev-cp-kafka:9092"
    bootstrap_servers = "localhost:9092"
    # schema_registry = "http://onestop-dev-cp-schema-registry:8081"
    schema_registry = "http://localhost:8081"

    base_conf = {
        'bootstrap.servers': bootstrap_servers,
        'schema.registry.url' : schema_registry
    }

    value = {
        "type": "granule",
        "content": "",
        "contentType": "application/json",
        "method": "PUT",
        "source": "unknown",
        "operation": "ADD"
    }

    key = "3244b32e-83a6-4239-ba15-199344ea5d9"

    data = {key: value}

    produce(base_conf, topic, data)


if __name__ == '__main__':
    unittest.main()