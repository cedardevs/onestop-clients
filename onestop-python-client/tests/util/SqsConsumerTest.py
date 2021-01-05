import unittest
import boto3
from moto import mock_sqs

from onestop.util.SqsConsumer import SqsConsumer

class SqsConsumerTest(unittest.TestCase):
    sc = None

    def setUp(self):
        print("Set it up!")
        self.sc = SqsConsumer("./config/aws-util-config-dev.yml", "./config/credentials-template.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.sc.conf['sqs_url']==None)

    @mock_sqs
    def test_poll_messages(self):
        # Create the mock queue beforehand and set its mock URL as the 'sqs_url' config value for SqsConsumer
        boto_session = boto3.Session(aws_access_key_id=self.sc.cred['sandbox']['access_key'],
                                     aws_secret_access_key=self.sc.cred['sandbox']['secret_key'])
        sqs_session = boto_session.resource('sqs', region_name=self.sc.conf['s3_region'])
        res = sqs_session.create_queue(QueueName="test_queue")
        self.sc.conf['sqs_url'] = res.url
        queue = self.sc.connect()
        self.sc.receive_messages(queue, self.sc.conf['sqs_max_polls'], lambda *args, **kwargs: None)


if __name__ == '__main__':
    unittest.main()