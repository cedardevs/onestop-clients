import argparse
import json
import os
import yaml

from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher
from onestop.schemas.util.jsonEncoder import EnumEncoder
from onestop.util.ClientLogger import ClientLogger

config_dict = {}

def handler(recs, log_level):
    '''
    Processes metadata information from sqs message triggered by S3 event and uploads to registry through web publisher (https). Also uploads s3 object to glacier.

    :param recs: dict
        sqs message triggered by s3 event

    :return: str
        IM registry response and boto3 glacier response
    '''

    logger = ClientLogger.get_logger('launch_e2e.handler', log_level, False)
    logger.info('In Handler')

    # If record exists try to get object-uuid retrieval
    logger.debug('Records:%s'%recs)
    if recs is None:
        logger.info('No records retrieved, doing nothing.')
        return

    rec = recs[0]
    logger.debug('Record: %s'%rec)
    bucket = rec['s3']['bucket']['name']
    s3_key = rec['s3']['object']['key']
    logger.info("Getting uuid")
    s3_resource = s3_utils.connect('resource', 's3', None)
    object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
    if object_uuid is not None:
        logger.info('Retrieved object-uuid: %s'% object_uuid)
    else:
        logger.info('UUID not found, adding uuid to bucket=%s key=%s'%(bucket, s3_key))
        s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

    s3ma = S3MessageAdapter(**config_dict)
    im_message = s3ma.transform(rec)
    logger.debug('S3MessageAdapter.transform: %s'%im_message)
    json_payload = json.dumps(im_message.to_dict(), cls=EnumEncoder)
    logger.debug('S3MessageAdapter.transform.json dump: %s'%json_payload)

    wp = WebPublisher(**config_dict)
    registry_response = wp.publish_registry("granule", object_uuid, json_payload, "POST")
    logger.debug('publish_registry response: %s'%registry_response.json())

    # Upload to archive
    file_data = s3_utils.read_bytes_s3(s3_client, bucket, s3_key)
    glacier = s3_utils.connect('client', 'glacier', config_dict['s3_region'])
    vault_name = config_dict['vault_name']

    resp_dict = s3_utils.upload_archive(glacier, vault_name, file_data)
    logger.debug('Upload to cloud, Response: %s'%resp_dict)
    if resp_dict == None:
        logger.error('Error uploading to s3 archive, see prior log statements.')
        return

    logger.info('upload archived location: %s'% resp_dict['location'])
    logger.info('archiveId: %s'% resp_dict['archiveId'])
    logger.info('sha256: %s'% resp_dict['checksum'])

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
    logger.debug('publish to registry response: %s'% registry_response)
    logger.info('Finished publishing to registry.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches e2e test")
    parser.add_argument('-conf', dest="conf", required=False, default='/etc/config/config.yml',
                        help="AWS config filepath")
    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Generate configuration dictionary
    conf_loc = args.pop('conf')
    with open(conf_loc) as f:
        config_dict.update(yaml.load(f, Loader=yaml.FullLoader))

    # Get credentials from passed in fully qualified path or ENV.
    cred_loc = args.pop('cred')
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

    config_dict.update({
        'registry_username' : registry_username,
        'registry_password' : registry_password,
        'access_key' : access_key,
        'secret_key' : access_secret
    })

    s3_utils = S3Utils(**config_dict)
    s3_client = s3_utils.connect('client', 's3', config_dict['s3_region'])

    # Upload test files to s3 bucket
    local_files = ["file1.csv", "file4.csv"]
    s3_file = None
    for file in local_files:
        local_file = "scripts/data/" + file
        # s3_file = "csv/" + file
        s3_file = "public/" + file
        if not s3_utils.upload_s3(s3_client, local_file, config_dict['s3_bucket'], s3_file, True):
            exit("Error setting up for e2e: The test files were not uploaded to the s3 bucket therefore the tests cannot continue.")

    # Receive s3 message and MVM from SQS queue
    sqs_consumer = SqsConsumer(**config_dict)
    sqs_resource = s3_utils.connect('resource', 'sqs', config_dict['s3_region'])
    queue = sqs_consumer.connect(sqs_resource, config_dict['sqs_name'])
    sqs_consumer.receive_messages(queue, config_dict['sqs_max_polls'], handler)
