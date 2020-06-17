from onestop.consumer import consume
import argparse

def handler(key, value):
    print(key)
    if (value['type'] == 'collection'):
        print(value['discovery']['fileIdentifier'])
    else:
        print(value['fileInformation']['name'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reogranizes granules matching a regex from one collection to another")
    parser.add_argument('-b', dest="bootstrap.servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema.registry.url", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-t', dest="topic", required=True,
                        help="Topic name")
    parser.add_argument('-g', dest="group.id", required=True,
                        help="Consumer group")
    parser.add_argument('-o', dest="auto.offset.reset", required=True,
                        help="offset")
    config = vars(parser.parse_args())
    topics = [config.pop('topic')]
    consume(config, topics, lambda k, v: handler(k, v))
