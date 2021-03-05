import argparse
import json
from onestop.KafkaConsumer import KafkaConsumer

def handler(key,value):
    print(key)
    print('VALUE-------')
    print(value)
    """
    if (value['type'] == 'collection' or not bool(value['fileInformation'])):
        print(value['discovery']['fileIdentifier'])
    else:
        print(value['fileInformation']['name'])
    """


if __name__ == '__main__':

    kafka_consumer = KafkaConsumer("scripts/config/kafka-publisher-config-dev.yml")
    metadata_consumer = kafka_consumer.connect()
    kafka_consumer.consume(metadata_consumer, lambda k, v: handler(k, v))
    """
    parser = argparse.ArgumentParser(description="Allows smeFunc to produce or consume messagges from kafkda topics")
    parser.add_argument('-cmd', dest="command", required=True,
                        help="Command (produce/consume)")
    
    parser.add_argument('-b', dest="bootstrap.servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema.registry.url", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-t', dest="topic", required=True,
                        help="Topic name")
    parser.add_argument('-g', dest="group.id", required=False,
                        help="Consumer group")
    parser.add_argument('-o', dest="auto.offset.reset", required=False,
                        help="offset")

    config = vars(parser.parse_args())
    topic = config.pop('topic')
    cmd = config.pop('command')
    
    if (cmd=="consume"):
        consume(config, topic, lambda k, v: handler(k, v))
        
        
    if (cmd=="produce"):
        
        #Example content
        value = {
            "type": "collection",
            "content": "Update!",
            "contentType": "application/json",
            "method": "PUT",
            "source": "unknown",
            "operation": "ADD"
        }

        key = "3ee5976e-789a-41d5-9cae-d51e7b92a247"

        data = {key: value}

        produce(config, topic, data)
    """

