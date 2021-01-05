import unittest

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

    def test_poll_messages(self):
        queue = self.sc.connect()
        self.sc.receive_messages(queue)


if __name__ == '__main__':
    unittest.main()