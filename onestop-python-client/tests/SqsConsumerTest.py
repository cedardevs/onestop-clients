import unittest

import json

from onestop.SqsConsumer import SqsConsumer

class SqsConsumerTest(unittest.TestCase):
    sc = None

    def setUp(self):
        print("Set it up!")
        self.sc = SqsConsumer("../config/sqs-consumer-config-dev.yml", "../config/sqs-credentials.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.sc.conf['sqs_url']==None)

    def test_poll_messages(self):
        queue = self.sc.connect()
        self.sc.receive_messges(queue)


if __name__ == '__main__':
    unittest.main()