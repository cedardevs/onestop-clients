import unittest

import json

from onestop.KafkaPublisher import KafkaPublisher

class KafkaPublisherTest(unittest.TestCase):
    kp = None

    def setUp(self):
        print("Set it up!")
        self.kp = KafkaPublisher("dev")
        print(str(self.kp.conf))


    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.kp.conf['brokers']==None)

    def test_blah(self):
        print("blah")
        # config = {
        #     'bootstrap.servers': self.bootstrap_servers,
        #     'schema.registry.url': self.schema_registry
        # }
        #
        # value = {
        #     "type": "granule",
        #     "content": "",
        #     "contentType": "application/json",
        #     "method": "PUT",
        #     "source": "unknown",
        #     "operation": "ADD"
        # }
        #
        # key = "3244b32e-83a6-4239-ba15-199344ea5d9"
        #
        # data = {key: value}
        #
        # #produce(config, self.topic, data)


if __name__ == '__main__':
    unittest.main()