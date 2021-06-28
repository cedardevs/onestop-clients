import argparse
import os
import yaml

from onestop.WebPublisher import WebPublisher
from onestop.util.S3Utils import S3Utils
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.SqsHandlers import create_delete_handler

config_dict = {}

if __name__ == '__main__':
    # All command-line arguments have defaults that use test data, with AWS mocking set to true
    parser = argparse.ArgumentParser(description="Launches SQS delete test")
    # Set default config location to the Helm mounted pod configuration location
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

    web_publisher = WebPublisher(**config_dict)
    s3_utils = S3Utils(**config_dict)
    sqs_consumer = SqsConsumer(**config_dict)

    sqs_max_polls = config_dict['sqs_max_polls']
    delete_handler = create_delete_handler(web_publisher)
    s3_resource = s3_utils.connect('resource', 'sqs', config_dict['s3_region'])
    queue = sqs_consumer.connect(s3_resource, config_dict['sqs_name'])

    sqs_consumer.receive_messages(queue, sqs_max_polls, delete_handler)
