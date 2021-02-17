import logging
from datetime import datetime, timezone
import yaml
import boto3
import json
from onestop.util.ClientLogger import ClientLogger


class SqsConsumer:
    conf = None

    def __init__(self, access_key, access_secret, s3_region, sqs_url, log_level = 'INFO'):

        self.access_key = access_key
        self.access_secret = access_secret
        self.s3_region = s3_region
        self.sqs_url = sqs_url
        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def connect(self):
        boto_session = boto3.Session(aws_access_key_id=self.access_key,
                                     aws_secret_access_key=self.access_secret)
        # Get the queue. This returns an SQS.Queue instance
        sqs_session = boto_session.resource('sqs', region_name=self.s3_region)
        self.logger.info("Connecting to " + self.sqs_url)
        sqs_queue = sqs_session.Queue(self.sqs_url)
        return sqs_queue

    def receive_messages(self, queue, sqs_max_polls, cb):
        self.logger.info("Receive messages")

        i = 1
        while i <= sqs_max_polls:
            self.logger.info("Polling attempt: " + str(i))
            i = i + 1

            #TODO MaxNumberOfMessages and WaitTimeSeconds configurable
            sqs_messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=10)
            self.logger.info("Received %d messages." % len(sqs_messages))

            for sqs_message in sqs_messages:
                try:
                    # Log start time
                    dt_start = datetime.now(tz=timezone.utc)
                    self.logger.info("Started processing message")

                    message_body = json.loads(sqs_message.body)
                    message_content = json.loads(message_body['Message'])

                    if 'Records' in message_content:
                        recs = message_content['Records']
                        self.logger.info("Received message")
                        self.logger.debug('Records: ' + str(recs))
                    else:
                        self.logger.info("s3 event without records content received.")

                    sqs_message.delete()

                    self.logger.info("The SQS message has been deleted.")

                    dt_end = datetime.now(tz=timezone.utc)
                    processing_time = dt_end - dt_start

                    self.logger.info("Completed processing message (s):" + str(processing_time.microseconds * 1000))
                    cb(recs)

                except:
                    self.logger.exception(
                        "An exception was thrown while processing a message, but this program will continue. The "
                        "message will not be deleted from the SQS queue. The message was: %s" % sqs_message.body)
