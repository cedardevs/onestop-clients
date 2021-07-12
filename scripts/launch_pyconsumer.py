import argparse
import os
import yaml
import json

from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher
from onestop.util.ClientLogger import ClientLogger
from onestop.schemas.util.jsonEncoder import EnumEncoder
from botocore.exceptions import ClientError

config_dict = {}

def handler(rec, log_level):
    '''
    Processes metadata information from sqs message triggered by S3 event and uploads to registry through web publisher (https). Utilizes helm for credentials and conf.

    :param rec: dict
        sqs message triggered by s3 event

    :return: str
        IM registry response
    '''
    logger = ClientLogger.get_logger('launch_pyconsumer.handler', log_level, False)
    logger.info('In Handler')

    # Now get boto client for object-uuid retrieval
    object_uuid = None

    if rec is None:
        logger.info('No record retrieved, doing nothing.')
        return

    bucket = rec['s3']['bucket']['name']
    s3_key = rec['s3']['object']['key']
    logger.debug('Rec: %s'%rec)
    # Fetch the object to get the uuid
    logger.info("Getting uuid")
    s3_resource = s3_utils.connect('resource', 's3', None)
    try:
        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
    except ClientError as e:
        logger.error(e)
        return

    if object_uuid is not None:
        logger.info('Retrieved object-uuid: %s'% object_uuid)
    else:
        logger.info('UUID not found, adding uuid to bucket=%s key=%s'%(bucket, s3_key))
        s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

    # Convert s3 message to IM message
    s3ma = S3MessageAdapter(**config_dict)
    im_message = s3ma.transform(rec)
    logger.debug('S3MessageAdapter.transform: %s'%im_message)
    json_payload = json.dumps(im_message.to_dict(), cls=EnumEncoder)
    logger.debug('S3MessageAdapter.transform.json dump: %s'%json_payload)

    #Send the message to Onestop
    wp = WebPublisher(**config_dict)
    registry_response = wp.publish_registry("granule", object_uuid, json_payload, "POST")
    logger.debug('publish_registry response: %s'%registry_response.json())

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

    # Receive s3 message and MVM from SQS queue
    sqs_consumer = SqsConsumer(**config_dict)
    sqs_resource = s3_utils.connect('resource', 'sqs', config_dict['s3_region'])
    queue = sqs_consumer.connect(sqs_resource, config_dict['sqs_name'])
    sqs_consumer.receive_messages(queue, config_dict['sqs_max_polls'], handler)
