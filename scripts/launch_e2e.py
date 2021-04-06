import argparse
import json
import os
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher
from onestop.extract.CsbExtractor import CsbExtractor
from onestop.schemas.util.jsonEncoder import EnumEncoder


def handler(recs):
    '''
    Processes metadata information from sqs message triggered by S3 event and uploads to registry through web publisher (https). Also uploads s3 object to glacier.

    :param recs: dict
        sqs message triggered by s3 event

    :return: str
        IM registry response and boto3 glacier response
    '''

    print("Handler...")

    # Now get boto client for object-uuid retrieval
    object_uuid = None
    bucket = None
    print(recs)
    if recs is None:
        print("No records retrieved")
    else:
        rec = recs[0]
        print(rec)
        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        print("Getting uuid")
        # High-level api
        s3_resource = s3_utils.connect("s3_resource", None)
        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
        if object_uuid is not None:
            print("Retrieved object-uuid: " + object_uuid)
        else:
            print("Adding uuid")
            s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

    im_message = s3ma.transform(recs)

    json_payload = json.dumps(im_message.to_dict(), cls=EnumEncoder)

    print(json_payload)


    registry_response = wp.publish_registry("granule", object_uuid, json_payload, "POST")
    #print(registry_response.json())

    # Upload to archive
    file_data = s3_utils.read_bytes_s3(s3_client, bucket, s3_key)
    glacier = s3_utils.connect("glacier", s3_utils.conf['s3_region'])
    vault_name = s3_utils.conf['vault_name']


    resp_dict = s3_utils.upload_archive(glacier, vault_name, file_data)

    print("archiveLocation: " + resp_dict['location'])
    print("archiveId: " + resp_dict['archiveId'])
    print("sha256: " + resp_dict['checksum'])

    addlocPayload = {
        "fileLocations": {
            resp_dict['location']: {
                "uri": resp_dict['location'],
                "type": "ACCESS",
                "restricted": True,
                "locality": "us-east-1",
                "serviceType": "Amazon:AWS:Glacier",
                "asynchronous": True
            }
        }
    }
    json_payload = json.dumps(addlocPayload, indent=2)
    # Send patch request next with archive location
    registry_response = wp.publish_registry("granule", object_uuid, json_payload, "PATCH")


if __name__ == '__main__':
    """
    parser = argparse.ArgumentParser(description="Launches e2e test")
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
    registry_user = os.environ.get("REGISTRY_USERNAME")
    registry_pwd = os.environ.get("REGISTRY_PASSWORD")
    print(registry_user)
    access_key = os.environ.get("AWS_ACCESS")
    access_secret = os.environ.get("AWS_SECRET")
    print(access_key)

    # High-level api
    s3_resource = s3_utils.connect("s3_resource", None)
    bucket = s3_utils.conf['s3_bucket']
    overwrite = True
    sqs_max_polls = s3_utils.conf['sqs_max_polls']
    # Add 3 files to bucket
    local_files = ["file1.csv", "file4.csv"]
    s3_file = None
    for file in local_files:
        local_file = "tests/data/" + file
        s3_file = "csv/" + file
        s3_utils.upload_s3(s3, local_file, bucket, s3_file, overwrite)
    # Receive s3 message and MVM from SQS queue
    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    s3ma = S3MessageAdapter("scripts/config/csb-data-stream-config.yml", s3_utils)
    # Retrieve data from s3 object
    #csb_extractor = CsbExtractor()
    wp = WebPublisher("config/web-publisher-config-dev.yml", cred_loc)
    queue = sqs_consumer.connect()
    try:
        debug = False
        sqs_consumer.receive_messages(queue, sqs_max_polls, handler)
    except Exception as e:
        print("Message queue consumption failed: {}".format(e))
    """

    parser = argparse.ArgumentParser(description="Launches e2e test")
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
    s3_client = s3_utils.connect("s3", None)

    bucket = s3_utils.conf['s3_bucket']

    sqs_max_polls = s3_utils.conf['sqs_max_polls']

    # Add 3 files to bucket
    local_files = ["file1.csv", "file4.csv"]
    s3_file = None
    for file in local_files:
        local_file = "data/" + file
        # s3_file = "csv/" + file
        s3_file = "NESDIS/CSB/" + file
        if not s3_utils.upload_s3(s3_client, local_file, bucket, s3_file, True):
            exit("Error setting up for e2e: The test files were not uploaded to the s3 bucket therefore the tests cannot continue.")

    # Receive s3 message and MVM from SQS queue
    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    s3ma = S3MessageAdapter("config/csb-data-stream-config.yml", s3_utils)
    wp = WebPublisher("config/web-publisher-config-dev.yml", cred_loc)

    queue = sqs_consumer.connect()
    try:
        debug = False
        sqs_consumer.receive_messages(queue, sqs_max_polls, handler)

    except Exception as e:
        print("Message queue consumption failed: {}".format(e))
