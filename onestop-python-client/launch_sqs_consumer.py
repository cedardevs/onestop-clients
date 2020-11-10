import argparse
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils

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

    #Use call back here?
    debug = True
    recs = sqs_consumer.receive_messages(queue, debug)

    # Now get boto client for object-uuid retrieval
    print("initializing from launch_sqs_consumer")
    s3_utils = S3Utils(conf_loc, cred_loc)

    boto_client = s3_utils.connect()

    if recs is None:
        print("No records retrieved")
    else:
        for rec in recs:
            print("message_content: " + str(rec))
            bucket = rec['s3']['bucket']['name']
            s3_key = rec['s3']['object']['key']

            obj_uuid = s3_utils.get_uuid_metadata(boto_client, bucket, s3_key)
            print("Retrieved object-uuid: " + obj_uuid)

    #queue.publish_collection(metadata_producer, collection_uuid, content_dict, method)

