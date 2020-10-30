import logging
from datetime import datetime, timezone
import yaml
import boto3

class SqsConsumer:
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = self.get_logger("SqsConsumer", False)
        self.logger.info('Initializing SqsConsumer')

    def get_logger(self, logger_name, create_file=False):

        # create logger
        log = logging.getLogger()

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.conf['log_level'] == "DEBUG":
            log.setLevel(level=logging.DEBUG)
        else:
            if self.conf['log_level'] == "INFO":
                log.setLevel(level=logging.INFO)
            else:
                log.setLevel(level=logging.ERROR)

        if create_file:
            # create file handler for logger.
            fh = logging.FileHandler('KafkaPublisher.log')
            fh.setFormatter(formatter)

        # create console handler for logger.
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # add handlers to logger.
        if create_file:
            log.addHandler(fh)

        log.addHandler(ch)
        return log

    def connect(self):
        boto_session = boto3.Session(aws_access_key_id=self.cred['access_key'],
                                     aws_secret_access_key=self.cred['secret_key'])
        # Get the queue. This returns an SQS.Queue instance
        sqs_session = boto_session.resource('sqs')
        sqs_queue = sqs_session.Queue(self.conf['sqs_url'])
        return sqs_queue

    def receive_messges(self, queue):
        self.logger.debug("Receive messages")
        while True:
            sqs_messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
            self.logger.debug("Received %d messages." % len(sqs_messages))

            for sqs_message in sqs_messages:
                try:
                    # Log start time
                    dt_start = datetime.now(tz=timezone.utc)
                    self.logger.info("Started processing message")

                    # jsonStringForOneStop = json.loads(sqsMessage.body)['Message']
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
                    self.logger.debug("The SQS message has been deleted.")

                    dt_end = datetime.now(tz=timezone.utc)
                    processing_time = dt_end - dt_start

                    self.logger.info("Completed processing message (s):" + str(processing_time.milliseconds * 1000))

                except:
                    self.logger.exception(
                        "An exception was thrown while processing a message, but this program will continue. The message will not be deleted from the SQS queue. The message was: %s" % sqsMessage.body)
