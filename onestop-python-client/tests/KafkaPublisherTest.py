import unittest

import json

from onestop.KafkaPublisher import KafkaPublisher

class KafkaPublisherTest(unittest.TestCase):
    kp = None

    def setUp(self):
        print("Set it up!")
        self.kp = KafkaPublisher("../config/kafka-publisher-config-dev.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.kp.conf['brokers']==None)

    def test_publish_collection(self):
        print("Publish collection")
        # Integration test TBD

if __name__ == '__main__':
    unittest.main()