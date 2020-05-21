
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
import os

def getSchema(config, topic):

    if config is not None :
        sr_conf = {key.replace("schema.registry.", ""): value.strip()
                   for key, value in config.items() if key.startswith("schema.registry")}

    if sr_conf is None or 'url' not in sr_conf:
        if 'SCHEMA_REGISTRY_URL' in os.environ:
            schema_registry_url = os.environ['SCHEMA_REGISTRY_URL']
            sr_conf['url'] = schema_registry_url

        else:
            raise ValueError('Required schema.registry.url not set. SCHEMA_REGISTRY_URL environment variable not set')

    sr = CachedSchemaRegistryClient(sr_conf)
    id, schema, version = sr.get_latest_schema(topic + "-value")

    return schema

