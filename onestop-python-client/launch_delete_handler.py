import json
import boto3
import argparse
from moto import mock_s3
from moto import mock_sqs
from tests.utils import create_delete_message
from onestop.WebPublisher import WebPublisher
from onestop.util.S3Utils import S3Utils
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.SqsHandlers import create_delete_handler


def mock_init_s3(s3u):
    """ Sets up bucket, object, SQS queue, and delete message.

    Assumes there are additional keys passed in via config

    :param s3u: S3Utils object
    :return: URL of the mock queue created in SQS
    """
    boto_client = s3u.connect("s3", None)
    bucket = s3u.conf['s3_bucket']
    region = s3u.conf['s3_region']
    key = s3u.conf['s3_key']
    boto_client.create_bucket(Bucket=bucket)
    boto_client.put_object(Bucket=bucket, Key=key, Body="foobar")

    sqs_client = boto3.client('sqs', region_name=region)
    sqs_queue = sqs_client.create_queue(QueueName=s3u.conf['sqs_name'])
    message = create_delete_message(region, bucket, key)
    sqs_client.send_message(QueueUrl=sqs_queue['QueueUrl'], MessageBody=json.dumps(message))
    return sqs_queue['QueueUrl']


if __name__ == '__main__':
    # All command-line arguments have defaults that use test data, with AWS mocking set to true
    parser = argparse.ArgumentParser(description="Launches SQS delete test")
    parser.add_argument('--aws-conf', dest="aws_conf", required=False, default="config/aws-util-config-test.yml",
                        help="AWS config filepath")
    parser.add_argument('--osim-conf', dest="osim_conf", required=False, default="config/web-publisher-config-local.yml",
                        help="OSIM config filepath")
    parser.add_argument('-mock', dest="mock", required=False, default=True, help="Use mock AWS or real values")

    parser.add_argument('-cred', dest="cred", required=False, default="config/credentials-template.yml",
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    wp_config = args.pop('osim_conf')
    aws_config = args.pop('aws_conf')
    cred_config = args.pop('cred')
    use_mocks = args.pop('mock')

    web_publisher = WebPublisher(wp_config, cred_config)
    s3_utils = S3Utils(aws_config, cred_config)
    sqs_consumer = SqsConsumer(aws_config, cred_config)

    if use_mocks is True:
        mock_1 = mock_s3()
        mock_2 = mock_sqs()
        mock_1.start()
        mock_2.start()
        mock_queue_url = mock_init_s3(s3_utils)
        # Need to override the config value here so that sqs_consumer.connect will use the correct url for the queue
        sqs_consumer.conf['sqs_url'] = mock_queue_url

    sqs_max_polls = s3_utils.conf['sqs_max_polls']
    delete_handler = create_delete_handler(web_publisher)

    queue = sqs_consumer.connect()
    try:
        sqs_consumer.receive_messages(queue, sqs_max_polls, delete_handler)
        if use_mocks is True:
            mock_1.stop()
            mock_2.stop()
    except Exception as e:
        print("Message queue consumption failed: {}".format(e))
        if use_mocks is True:
            mock_1.stop()
            mock_2.stop()
