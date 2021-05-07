import json

from datetime import datetime, timezone
from onestop.util.ClientLogger import ClientLogger

class SqsConsumer:
    """
    A class used to consume messages from sqs queue

    Attributes
    ----------
        logger: ClientLogger object
                utilizes python logger library and creates logging for our specific needs

    Methods
    -------
        receive_messages(sqs_client, sqs_queue_name, sqs_max_polls, cb)
            polls for messages in the queue
    """

    def __init__(self, log_level = 'INFO', **wildargs):
        """
        Attributes
        ----------
            log_level: str
                The log level to use for this class (Defaults to 'INFO')
        """
        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
        self.logger.info("Initializing " + self.__class__.__name__)

        if wildargs:
            self.logger.error("There were extra constructor arguments: " + str(wildargs))

    def receive_messages(self, sqs_client, sqs_queue_name, sqs_max_polls, cb):
        """
        Polls for messages from an sqs queue

        :param sqs_client: boto SQS.Client
            instance of boto sqs Client
        :param sqs_queue_name: str
            name of the queue to connect to.
        :param sqs_max_polls: int
            number of polls
        :param cb: function
            call back function

        :return: If the Message has a Records key then the call back function gets called on the Message.

        """
        self.logger.info("Receive messages")
        self.logger.info("Polling %d time(s) for SQS messages" % sqs_max_polls)

        sqs_queue = sqs_client.Queue(sqs_queue_name)

        i = 1
        while i <= sqs_max_polls:
            self.logger.info("Polling attempt: " + str(i))
            i = i + 1

            sqs_messages = sqs_queue.receive_messages(
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10
            )
            self.logger.info("Received %d messages." % len(sqs_messages))
            self.logger.debug("Messages: %s" % sqs_messages)

            for sqs_message in sqs_messages:
                try:
                    # Log start time
                    dt_start = datetime.now(tz=timezone.utc)
                    self.logger.info("Starting processing message")
                    self.logger.debug("Message: %s" % sqs_message)
                    self.logger.debug("Message body: %s" % sqs_message.body)

                    message_body = json.loads(sqs_message.body)
                    self.logger.debug("Message body message: %s" % message_body['Message'])
                    message_content = json.loads(message_body['Message'])

                    if 'Records' in message_content:
                        recs = message_content['Records']
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
