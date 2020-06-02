import unittest
import json

from tests.sqs_handler import SQSHandler
from tests import SqsMockAWS
from examples import sqsProducer


class TestSQSHandler(SqsMockAWS):

    def setUp(self):
        super(TestSQSHandler, self).setUp()
        self.sqs_handler = SQSHandler()
        self.sqs.meta.client.purge_queue(QueueUrl="test_query")

    def test_receive_messages_from_queue__returns_None_when_no_messages_found(self):
        message = self.sqs_handler.receive_messages_from_queue("test_query", 1)
        self.assertEqual(message, None)

    def test_add_message_to_retrieve_messages_from_queue__returns_message(self):
        payload = {"discovery": {"fileIdentifier": "92ade5dc-946d-11ea-abe4-0242ac120004", "links": [
            {"linkFunction": "download", "linkName": "Amazon S3", "linkProtocol": "HTTPS",
             "linkUrl": "https://s3.amazonaws.com/nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2"}],
                                 "parentIdentifier": "0fad03df-0805-434a-86a6-7dc42d68480f", "spatialBounding": None,
                                 "temporalBounding": {"beginDate": "2020-05-12T16:20:15.158Z",
                                                      "endDate": "2020-05-12T16:21:51.494Z"},
                                 "title": "HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2"},
                   "fileInformation": {"format": "HSD", "name": "HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2",
                                       "size": 208918}, "fileLocations": {
                "s3://nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2": {
                    "asynchronous": False, "deleted": False, "lastModified": 1589300890000, "locality": "us-east-1",
                    "restricted": False, "serviceType": "Amazon:AWS:S3", "type": "ACCESS",
                    "uri": "s3://nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2"}},
                   "relationships": [{"id": "0fad03df-0805-434a-86a6-7dc42d68480f", "type": "COLLECTION"}]}
        # add message to queue
        self.sqs_handler.add_message_to_queue("test_query", payload)

        messages = sqsProducer.sqs_receive_publish()
        # messages = self.sqs_handler.receive_messages_from_queue(queue_url="test_query")

        message_body = json.loads(messages[0]['Body'])

        self.assertEqual(len(messages), 1)
        self.assertEqual(message_body, payload)


if __name__ == '__main__':
    unittest.main()

# topic = "psi-granule-input-unknown"
# # bootstrap_servers = "onestop-dev-cp-kafka:9092"
# bootstrap_servers = "localhost:9092"
# # schema_registry = "http://onestop-dev-cp-schema-registry:8081"
# schema_registry = "http://localhost:8081"
#
# base_conf = {{
#     #     "type": "granule",
#     #     "content": "",
#     #     "contentType": "application/json",
#     #     "method": "PUT",
#     #     "source": "unknown",
#     #     "operation": "ADD"
#     # }
#     'bootstrap.servers': bootstrap_servers,
#     'schema.registry.url' : schema_registry
# }
#
# key = "3244b32e-83a6-4239-ba15-199344ea5d9"
# test =
#
# data = {key: test}
#
# produce(base_conf, topic, data)
