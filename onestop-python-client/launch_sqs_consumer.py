import argparse
from onestop.KafkaPublisher import KafkaPublisher

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches SqsConsumer to receive SQS messages")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="Config filepath")
    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    conf_loc = args.pop('conf')
    cred_loc = args.pop('cred')



    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    queue = sqs_consumer.connect()
    queue.publish_collection(metadata_producer, collection_uuid, content_dict, method)

