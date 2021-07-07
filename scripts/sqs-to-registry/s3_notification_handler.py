import os
import yaml
import json

from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher
from onestop.util.SqsHandlers import create_delete_handler
from onestop.util.SqsHandlers import create_upload_handler
from onestop.util.ClientLogger import ClientLogger

import argparse

config_dict = {}


def handler(recs, log_level):
    logger = ClientLogger.get_logger('s3_notification_handler.handler', log_level, False)
    logger.info('In Handler')

    if recs is None:
        logger.info('No records retrieved, doing nothing.')
        return

    rec = recs[0]
    logger.info('Record:%s'%rec)

    if 'ObjectRemoved' in rec['eventName']:
        delete_handler(recs)
    else:
        upload_handler(recs)

if __name__ == '__main__':
    # Example command: python3 archive_client_integration.py -conf /Users/whoever/repo/onestop-clients/scripts/config/combined_template.yml -cred /Users/whoever/repo/onestop-clients/scripts/config/credentials.yml
    #    python3 archive_client_integration.py -cred /Users/whoever/repo/onestop-clients/scripts/config/credentials.yml
    parser = argparse.ArgumentParser(description="Launches archive client integration")
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
    sqs_consumer = SqsConsumer(**config_dict)

    wp = WebPublisher(**config_dict)

    s3_utils = S3Utils(**config_dict)

    s3ma = S3MessageAdapter(**config_dict)

    delete_handler = create_delete_handler(wp)
    upload_handler = create_upload_handler(wp, s3_utils, s3ma)

    s3_resource = s3_utils.connect('resource', 'sqs',  config_dict['s3_region'])
    queue = sqs_consumer.connect(s3_resource, config_dict['sqs_name'])

    # Send a test message
    test_message = {
        "Type": "Notification",
        "MessageId": "e12f0129-0236-529c-aeed-5978d181e92a",
        "TopicArn": "arn:aws:sns:" + config_dict['s3_region'] + ":798276211865:cloud-archive-client-sns",
        "Subject": "Amazon S3 Notification",
        "Message": '''{
                "Records": [{
                    "eventVersion": "2.1", "eventSource": "aws:s3", "awsRegion": "''' + config_dict['s3_region'] + '''",
                    "eventTime": "2020-12-14T20:56:08.725Z", 
                    "eventName": "ObjectRemoved:Delete",
                    "userIdentity": {"principalId": "AX8TWPQYA8JEM"},
                    "requestParameters": {"sourceIPAddress": "65.113.158.185"},
                    "responseElements": {"x-amz-request-id": "D8059E6A1D53597A",
                                         "x-amz-id-2": "7DZF7MAaHztZqVMKlsK45Ogrto0945RzXSkMnmArxNCZ+4/jmXeUn9JM1NWOMeKK093vW8g5Cj5KMutID+4R3W1Rx3XDZOio"},
                    "s3": {
                        "s3SchemaVersion": "1.0", "configurationId": "archive-testing-demo-event",
                        "bucket": {"name": "''' + config_dict['s3_bucket'] + '''",
                                   "ownerIdentity": {"principalId": "AX8TWPQYA8JEM"},
                                   "arn": "arn:aws:s3:::''' + config_dict['s3_bucket'] + '''"},
                        "object": {"key": "123", 
                                   "sequencer": "005FD7D1765F04D8BE",
                                   "eTag": "44d2452e8bc2c8013e9c673086fbab7a",
                                   "size": 1385,
                                   "versionId": "q6ls_7mhqUbfMsoYiQSiADnHBZQ3Fbzf"}
                    }
                }]
            }''',
        "Timestamp": "2020-12-14T20:56:23.786Z",
        "SignatureVersion": "1",
        "Signature": "MB5P0H5R5q3zOFoo05lpL4YuZ5TJy+f2c026wBWBsQ7mbNQiVxAy4VbbK0U1N3YQwOslq5ImVjMpf26t1+zY1hoHoALfvHY9wPtc8RNlYqmupCaZgtwEl3MYQz2pHIXbcma4rt2oh+vp/n+viARCToupyysEWTvw9a9k9AZRuHhTt8NKe4gpphG0s3/C1FdvrpQUvxoSGVizkaX93clU+hAFsB7V+yTlbKP+SNAqP/PaLtai6aPY9Lb8reO2ZjucOl7EgF5IhBVT43HhjBBj4JqYBNbMPcId5vMfBX8qI8ANIVlGGCIjGo1fpU0ROxSHsltuRjkmErpxUEe3YJJM3Q==",
        "SigningCertURL": "https://sns.us-east-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
        "UnsubscribeURL": "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:798276211865:cloud-archive-client-sns:461222e7-0abf-40c6-acf7-4825cef65cce"
    }

#    sqs_client = s3_utils.connect('client', 'sqs' , config_dict['s3_region'])
#    sqs_client.send_message(
#        QueueUrl='https://sqs.us-east-2.amazonaws.com/798276211865/cloud-archive-client-sqs',
#        MessageBody=json.dumps(test_message)
#    )

    #Hack to make this stay up forever
    #TODO add feature to client library for polling indefinitely
    while True:
        sqs_consumer.receive_messages(queue, config_dict['sqs_max_polls'], handler)
