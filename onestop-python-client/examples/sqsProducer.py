import json
import logging
import sys
import boto3
import requests
# This is a custom submodule that is part of a larger module used in the nesdis-pghpc environment.
import pgutil.logging
from onestop_client.producer import produce

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
pgutil.logging.attachStreamHandlerToLogger(logging.getLogger())

if len(sys.argv) != 6:
    raise Exception("Usage: %s <nodeRoleName> <sqsQueueUrl> <kafkaBrokerHostAndPort> <schemaRegistryUrl> <topic>")

roleName = sys.argv[1]
sqsQueueUrl = sys.argv[2]
kafkaBrokerHostAndPort = sys.argv[3]
schemaRegistryUrl = sys.argv[4]
topic = sys.argv[5]

# Use the EC2 instance metadata API to get session credentials based on the node role
sessionResponse = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/{}".format(roleName))
sessionJson = sessionResponse.json()
botoSession = boto3.Session(
    aws_access_key_id=sessionJson["AccessKeyId"],
    aws_secret_access_key=sessionJson["SecretAccessKey"],
    aws_session_token=sessionJson["Token"]
)
SQS_RESOURCE = botoSession.resource('sqs')
jsonMessagesQueue = SQS_RESOURCE.Queue(sqsQueueUrl)

while True:
    sqsMessages = jsonMessagesQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
    logger.debug("Received %d messages." % len(sqsMessages))

    for sqsMessage in sqsMessages:
        try:
            processMessageTimer = pgutil.logging.CodeSegmentTimer("Processing message")
            jsonStringForOneStop = json.loads(sqsMessage.body)['Message']
            logger.debug("Retrieved JSON metadata from message body: %s" % jsonStringForOneStop)
            fileId = json.loads(jsonStringForOneStop)['discovery']['fileIdentifier']

            producer_conf = {
                'bootstrap.servers': kafkaBrokerHostAndPort,
                'schema.registry.url' : schemaRegistryUrl
            }

            rawInputMessage = {
                "type": "granule",
                "content": jsonStringForOneStop,
                "contentType": "application/json",
                "method": "PUT",
                "source": "unknown",
                "operation": "ADD"
            }

            logger.debug("Will push the metadata to \"%s\"." % topic)
            messageMap = {fileId : rawInputMessage}
            produce(producer_conf, topic, rawInputMessage)

            sqsMessage.delete()
            logger.debug("The SQS message has been deleted.")
            processMessageTimer.finishAndPrintTime()

        except:
            logger.exception("An exception was thrown while processing a message, but this program will continue. The message will not be deleted from the SQS queue. The message was: %s" % sqsMessage.body)
