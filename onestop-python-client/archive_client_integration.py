import argparse
import json
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher

def handler(recs):
    print("Handler...")

    # Now get boto client for object-uuid retrieval
    object_uuid = None
    bucket = None

    if recs is None:
        print( "No records retrieved" )
    else:
        rec = recs[0]
        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        print('Bucket: ' + str(bucket))
        print('s3_key: ' + str(s3_key))

        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
        if object_uuid is not None:
            print("Retrieved object-uuid: " + object_uuid)
        else:
            print("Adding uuid")
            s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches archive client integration")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="AWS config filepath")

    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Get configuration file path locations
    conf_loc = args.pop('conf')
    cred_loc = args.pop('cred')

    # Upload a test file to s3 bucket
    s3_utils = S3Utils(conf_loc, cred_loc)

    # Low-level api ? Can we just use high level revisit me!
    s3 = s3_utils.connect("s3", None)

    # High-level api
    s3_resource = s3_utils.connect("s3_resource", None)

    bucket = s3_utils.conf['s3_bucket']
    overwrite = True


    sqs_max_polls = s3_utils.conf['sqs_max_polls']

    # Receive s3 message and MVM from SQS queue
    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    s3ma = S3MessageAdapter("config/csb-data-stream-config.yml")
    wp = WebPublisher("config/web-publisher-config-dev.yml", cred_loc)

    queue = sqs_consumer.connect()
    try:
        debug = False
        sqs_consumer.receive_messages(queue, sqs_max_polls, handler)

    except Exception as e:
        print("Message queue consumption failed: {}".format(e))