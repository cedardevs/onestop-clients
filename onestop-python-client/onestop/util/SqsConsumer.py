import logging
from datetime import datetime, timezone
import yaml
import boto3
import json
from onestop.util import ClientLogger


class SqsConsumer:
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, "DEBUG", False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def connect(self):
        boto_session = boto3.Session(aws_access_key_id=self.cred['sandbox']['access_key'],
                                     aws_secret_access_key=self.cred['sandbox']['secret_key'])
        # Get the queue. This returns an SQS.Queue instance
        sqs_session = boto_session.resource('sqs', region_name=self.conf['region'])
        sqs_queue = sqs_session.Queue(self.conf['sqs_url'])
        return sqs_queue

    def receive_messages(self, queue):
        self.logger.info("Receive messages")
        continue_polling = True

        while continue_polling:
            sqs_messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=10)
            self.logger.info("Received %d messages." % len(sqs_messages))
            records_content = []

            for sqs_message in sqs_messages:
                try:
                    # Log start time
                    dt_start = datetime.now(tz=timezone.utc)
                    self.logger.info("Started processing message")

                    message_content = json.loads(sqs_message.body)

                    if 'Records' in message_content:
                        recs = message_content['Records']
                    else:
                        self.logger.info("s3 event without records content received.")

                    # Grab osim-uuid here

                    # Translate to IM message format

                    # self.logger.debug("Retrieved JSON metadata from message body: %s" % jsonStringForOneStop)
                    #
                    # fileMetadataUrl = baseMetadataUrl + '/' + json.loads(jsonStringForOneStop)['discovery'][
                    #     'fileIdentifier']
                    # self.logger.debug("Will push the metadata to \"%s\"." % fileMetadataUrl)
                    #
                    # response = requests.put(fileMetadataUrl, headers={'Content-Type': "application/json"},
                    #                         data=jsonStringForOneStop)
                    # logger.debug("HTTP PUT response status code: %d. Response body: %s", response.status_code,
                    #              response.text)
                    # response.raise_for_status()

                    sqs_message.delete()

                    self.logger.info("The SQS message has been deleted.")

                    dt_end = datetime.now(tz=timezone.utc)
                    processing_time = dt_end - dt_start

                    self.logger.info("Completed processing message (s):" + str(processing_time.microseconds * 1000))
                    return recs

                except:
                    self.logger.exception(
                        "An exception was thrown while processing a message, but this program will continue. The "
                        "message will not be deleted from the SQS queue. The message was: %s" % sqs_message.body)

            print("continue_polling:" + str(continue_polling))