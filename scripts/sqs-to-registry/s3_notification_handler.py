import os
import yaml
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher
from onestop.util.SqsHandlers import create_delete_handler
from onestop.util.SqsHandlers import create_upload_handler
from onestop.util.SqsHandlers import create_copy_handler

from datetime import date
import argparse

def handler(recs):
    print("Handling message...")

    # Now get boto client for object-uuid retrieval
    object_uuid = None

    if recs is None:
        print("No records retrieved" + date.today())
    else:
        rec = recs[0]
        print(rec)
        if 'ObjectRemoved' in rec['eventName']:
            print("SME - calling delete handler")
            print(rec['eventName'])
            delete_handler(recs)
        else:
            print("SME - calling upload handler")
            upload_handler(recs)
            #copy_handler(recs)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Launch SQS to Registry consumer")
    parser.add_argument('-conf', dest="conf", required=False,
                        help="Config filepath")

    parser.add_argument('-cred', dest="cred", required=False,
                        help="Credentials filepath")

    args = vars(parser.parse_args())
    cred_loc = args.pop('cred')

    #credentials from either file or env
    registry_username = None
    registry_password = None
    access_key = None
    access_secret = None

    if cred_loc is not None:
        with open(cred_loc) as f:
            creds = yaml.load(f, Loader=yaml.FullLoader)
        registry_username = creds['registry']['username']
        registry_password = creds['registry']['password']
        access_key = creds['sandbox']['access_key']
        access_secret = creds['sandbox']['secret_key']
    else:
        print("Using env variables for config parameters")
        registry_username = os.environ.get("REGISTRY_USERNAME")
        registry_password = os.environ.get("REGISTRY_PASSWORD")
        access_key = os.environ.get("ACCESS_KEY")
        access_secret = os.environ.get("SECRET_KEY")

    # default config location mounted in pod
    if args.pop('conf') is None:
        conf_loc = "/etc/config/config.yml"
    else:
        conf_loc = args.pop('conf')

    conf = None
    with open(conf_loc) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    #TODO organize the config
    #System
    log_level = conf['log_level']
    sqs_max_polls = conf['sqs_max_polls']

    #Destination
    registry_base_url = conf['registry_base_url']
    onestop_base_url = conf['onestop_base_url']

    #Source
    access_bucket = conf['access_bucket']
    sqs_url = conf['sqs_url']
    s3_region = conf['s3_region']
    s3_bucket2 = conf['s3_bucket2']
    s3_region2 = conf['s3_region2']


    #Onestop related
    prefix_map = conf['prefixMap']
    file_id_prefix = conf['file_identifier_prefix']
    file_format = conf['format']
    headers = conf['headers']
    type = conf['type']

    sqs_consumer = SqsConsumer(access_key, access_secret, s3_region, sqs_url, log_level)

    wp = WebPublisher(registry_base_url=registry_base_url, username=registry_username, password=registry_password,
                      onestop_base_url=onestop_base_url, log_level=log_level)

    s3_utils = S3Utils(access_key, access_secret, log_level)
    s3ma = S3MessageAdapter(access_bucket, prefix_map, format, headers, type, file_id_prefix, log_level)

    delete_handler = create_delete_handler(wp)
    upload_handler = create_upload_handler(wp, s3_utils, s3ma)

    #TODO this is going away in favor of replication at the bucket level
    copy_handler = create_copy_handler(wp, s3_utils, s3ma, destination_bucket=s3_bucket2, destination_region=s3_region2)

    queue = sqs_consumer.connect()

    try:
        debug = False
        # # Pass in the handler method
        #Hack to make this stay up forever
        #TODO add feature to client library for polling indefinitely
        while True:
            sqs_consumer.receive_messages(queue, sqs_max_polls, handler)

    except Exception as e:
        print("Message queue consumption failed: {}".format(e))
