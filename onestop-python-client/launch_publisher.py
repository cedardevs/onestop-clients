import argparse
from onestop.KafkaPublisher import KafkaPublisher



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches KafkaPublisher to publish kafkda topics")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="Config filepath")

    args = vars(parser.parse_args())

    confLoc = args.pop('conf')

    kafka_publisher = KafkaPublisher(confLoc)
    #kafka_publisher.connect()

