# from  producer import produce
import unittest

import boto3
from moto import mock_sqs


class SqsMockAWS(unittest.TestCase):
    def setUp(self):
        self.sqs_mock = mock_sqs()
        self.sqs_mock.start()

        self.sqs = boto3.resource('sqs')
        self.sqs.create_queue(QueueName=f"test_query")

    def tearDown(self):
        self.sqs_mock.stop()
