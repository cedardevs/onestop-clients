import json
import logging
import sys
import boto3
import requests
# This is a custom submodule that is part of a larger module used in the nesdis-pghpc environment.
import pgutil.logging
from producer.producer import produce
from argparse import ArgumentParser


def sqs_command_line_args():
    arg_parser = ArgumentParser(description='add sqs related values ... ')

    arg_parser.add_argument('--nodeRoleName', required=False, default='admin', help='role name')
    arg_parser.add_argument('--sqsQueueUrl', required=False, default='test_query', help='sqs url')
    arg_parser.add_argument('--bootstrapServers', required=False, default='localhost:9092',
                            help='Bootstrap server address')
    arg_parser.add_argument('--schemaRegistry', required=False, default='http://localhost:8081',
                            help='Schema Registry url')
    arg_parser.add_argument('--topicName', required=False, default='psi-granule-input-unknown', help='Topic name')

    values = arg_parser.parse_args()

    return values


def collect_sqs_messages(role_name, sqs_queue_url):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    pgutil.logging.attachStreamHandlerToLogger(logging.getLogger())

    # Use the EC2 instance metadata API to get session credentials based on the node role
    sessionResponse = requests.get(
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/{}".format(role_name))
    sessionJson = sessionResponse.json()
    botoSession = boto3.Session(
        aws_access_key_id=sessionJson["AccessKeyId"],
        aws_secret_access_key=sessionJson["SecretAccessKey"],
        aws_session_token=sessionJson["Token"]
    )
    SQS_RESOURCE = botoSession.resource('sqs')
    jsonMessagesQueue = SQS_RESOURCE.Queue(sqs_queue_url)

    data = {}

    while True:
        sqsMessages = jsonMessagesQueue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=2)
        logger.debug("Received %d messages." % len(sqsMessages))
        print(sqsMessages.body)
        #
        for sqsMessage in sqsMessages:
            try:
                processMessageTimer = pgutil.logging.CodeSegmentTimer("Processing message")
                jsonStringForOneStop = json.loads(sqsMessage)  # json.loads(sqsMessage.body)[0]
                print(jsonStringForOneStop)
                logger.debug("Retrieved JSON metadata from message body: %s" % jsonStringForOneStop)
                fileId = json.loads(jsonStringForOneStop)['discovery']['fileIdentifier']

                rawInputMessage = {
                    "type": "granule",
                    "content": jsonStringForOneStop,
                    "contentType": "application/json",
                    "method": "PUT",
                    "source": "unknown",
                    "operation": "ADD"
                }

                logger.debug("Will push the metadata for \"%s\"." % fileId)
                data[fileId] = rawInputMessage

                sqsMessage.delete()
                logger.debug("The SQS message has been deleted.")
                processMessageTimer.finishAndPrintTime()

            except:
                logger.exception(
                    "An exception was thrown while processing a message,"
                    " but this program will continue. The message will not be deleted from the SQS queue. "
                    "The message was: %s" % sqsMessage.body)
        return data


if __name__ == '__main__':
    if len(sys.argv) != 6:
        raise Exception("Usage: %s <nodeRoleName> <sqsQueueUrl> <kafkaBrokerHostAndPort> <schemaRegistryUrl> <topic>")
    else:
        config = sqs_command_line_args()

    roleName = config.nodeRoleName
    sqsQueueUrl = config.sqsQueueUrl
    bootstrapServers = config.bootstrapServers
    schemaRegistryUrl = config.schemaRegistry
    topic = config.topicName

    # roleName = 'admin' #config.node_role_name
    # sqsQueueUrl = 'test_query'  # config.sqs_queue_url
    # bootstrapServers = 'localhost:9092'  # config.bootstrap_servers
    # schemaRegistryUrl = 'http://localhost:8081'  # config.schema_registry
    # topic = 'psi-granule-input-unknown'  # config.topic_name

    base_conf = {
        'bootstrap.servers': bootstrapServers,
        'schema.registry.url': schemaRegistryUrl
    }

    data = collect_sqs_messages(roleName, sqsQueueUrl)

    produce(topic, data, base_conf)
