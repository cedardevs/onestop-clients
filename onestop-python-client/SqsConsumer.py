import json
import logging
import sys

from datetime import timezone
from datetime import datetime
from datetime import timedelta

import boto3
import requests

#
logger = logging.getLogger(__name__)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

if len(sys.argv) != 4:
    print("Usage: %s <nodeRoleName> <sqsQueueUrl> <psiRegistryApiRoot>")
    raise Exception("Usage: %s <nodeRoleName> <sqsQueueUrl> <psiRegistryApiRoot>")

# roleName = sys.argv[1]
# sqsQueueUrl = sys.argv[2]
# psiRegistryApiRoot = sys.argv[3]
#
# # Use the EC2 instance metadata API to get session credentials based on the node role
# sessionResponse = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/{}".format(roleName))
# sessionJson = sessionResponse.json()
# botoSession = boto3.Session(
# 	aws_access_key_id=sessionJson["AccessKeyId"],
# 	aws_secret_access_key=sessionJson["SecretAccessKey"],
# 	aws_session_token=sessionJson["Token"]
# )
# SQS_RESOURCE = botoSession.resource('sqs')
# jsonMessagesQueue = SQS_RESOURCE.Queue(sqsQueueUrl)
# baseMetadataUrl = "%s/metadata/granule" % (psiRegistryApiRoot)
#
# while True:
# 	sqsMessages = jsonMessagesQueue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
logger.debug("test debug")
#logger.debug("Received %d messages." % len(sqsMessages))

	# for sqsMessage in sqsMessages:
	# 	try:
	# 		#Log start time
	# 		dt_start = datetime.now(tz=timezone.utc)
	# 		logger.info("Started processing message")
    #
	# 		jsonStringForOneStop = json.loads(sqsMessage.body)['Message']
	# 		logger.debug("Retrieved JSON metadata from message body: %s" % jsonStringForOneStop)
    #
	# 		fileMetadataUrl = baseMetadataUrl + '/' + json.loads(jsonStringForOneStop)['discovery']['fileIdentifier']
	# 		logger.debug("Will push the metadata to \"%s\"." % fileMetadataUrl)
    #
	# 		response = requests.put(fileMetadataUrl, headers={'Content-Type': "application/json"}, data=jsonStringForOneStop)
	# 		logger.debug("HTTP PUT response status code: %d. Response body: %s", response.status_code, response.text)
	# 		response.raise_for_status()
    #
	# 		sqsMessage.delete()
	# 		logger.debug("The SQS message has been deleted.")
    #
	# 		dt_end = datetime.now(tz=timezone.utc)
	# 		processing_time = dt_end - dt_start
    #
	# 		logger.info("Completed processing message (s):" + str(processing_time.milliseconds * 1000))
    #
	# 	except:
	# 		logger.exception("An exception was thrown while processing a message, but this program will continue. The message will not be deleted from the SQS queue. The message was: %s" % sqsMessage.body)
