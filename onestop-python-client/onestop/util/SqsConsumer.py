import logging
from datetime import datetime, timezone
import yaml
import boto3
import json
from onestop.util.ClientLogger import ClientLogger


class SqsConsumer:
    """
    A class used to consume messages from sqs queue

    Attributes
    ----------
    conf: yaml file
        aws-util-config-dev.yml
    cred: yaml file
        credentials.yml
    logger: ClientLogger object
            utilizes python logger library and creates logging for our specific needs
    logger.info: ClientLogger object
        logging statement that occurs when the class is instantiated

    Methods
    -------
    connect()
        connects a boto sqs instance based on configurations in conf and cred yml files

    receive_messages(queue, sqs_max_polls, cb)
        polls for messages in the queue
    """
    conf = None

    def __init__(self, conf_loc, cred_loc):
        """

        :param conf_loc: yaml file
            aws-util-config-dev.yml
        :param cred_loc: yaml file
            credentials.yml

        Other Attributes
        ----------------
        logger: ClientLogger object
            utilizes python logger library and creates logging for our specific needs
        logger.info: ClientLogger object
            logging statement that occurs when the class is instantiated

        """
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def connect(self):
        """
        Connects a boto sqs instance based on configurations in conf and cred yml files

        :return: boto sqs
            returns instance of boto sqs resource
        """
        boto_session = boto3.Session(aws_access_key_id=self.cred['sandbox']['access_key'],
                                     aws_secret_access_key=self.cred['sandbox']['secret_key'])
        # Get the queue. This returns an SQS.Queue instance
        sqs_session = boto_session.resource('sqs', region_name=self.conf['s3_region'])
        sqs_queue = sqs_session.Queue(self.conf['sqs_url'])
        self.logger.info("Connecting to " + self.conf['sqs_url'])
        return sqs_queue

    def receive_messages(self, queue, sqs_max_polls, cb):
        """
        Polls for messages in the queue

        :param queue: boto sqs resource
            instance of boto sqs resource given from connect()
        :param sqs_max_polls: int
            number of polls
        :param cb: function
            call back function

        :return: Dependent on the call back function

        """
        self.logger.info("Receive messages")

        i = 1
        while i <= sqs_max_polls:
            self.logger.info("Polling attempt: " + str(i))
            i = i + 1

            sqs_messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=10)
            self.logger.info("Received %d messages." % len(sqs_messages))

            for sqs_message in sqs_messages:
                try:
                    print('IN Try')
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
