import json
import unittest

from unittest import mock
from unittest.mock import patch
from moto import mock_sqs
from tests.utils import abspath_from_relative, create_delete_message
from onestop.WebPublisher import WebPublisher
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.SqsHandlers import create_delete_handler


class SqsHandlerTest(unittest.TestCase):

    def setUp(self):
        print("Set it up!")

        self.config_dict = {
            'access_key': 'test_access_key',
            'secret_key': 'test_secret_key',
            'access_bucket': 'https://archive-testing-demo.s3-us-east-2.amazonaws.com',
            'type': 'COLLECTION',
            'file_id_prefix': 'gov.noaa.ncei.csb:',
            'collection_id': 'fdb56230-87f4-49f2-ab83-104cfd073177',
            'registry_base_url': 'http://localhost/onestop/api/registry',
            'registry_username': 'admin',
            'registry_password': 'whoknows',
            'onestop_base_url': 'http://localhost/onestop/api/search/search',
            'log_level': 'DEBUG'
        }

        self.wp = WebPublisher(**self.config_dict)
        self.s3_utils = S3Utils(**self.config_dict)
        self.s3ma = S3MessageAdapter(**self.config_dict)
        self.sqs_consumer = SqsConsumer(**self.config_dict)

        self.sqs_max_polls = 3
        self.region = 'us-east-2'
        self.bucket = 'archive-testing-demo'
        self.key = 'ABI-L1b-RadF/2019/298/15/OR_ABI-L1b-RadF-M6C15_G16_s20192981500369_e20192981510082_c20192981510166.nc'

    def tearDown(self):
        print("Tear it down!")

    def mocked_search_response_data(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        print ("args: "+str(args)+" kwargs: "+str(kwargs))
        onestop_search_response = {
            "data":[
                {
                    "attributes":{
                        "serviceLinks":[

                        ],
                        "citeAsStatements":[

                        ],
                        "links":[
                            {
                                "linkFunction":"download",
                                "linkUrl":"s3://archive-testing-demo-backup/public/NESDIS/CSB/csv/2019/12/01/20191201_08d5538c6f8dbefd7d82929623a34385_pointData.csv",
                                "linkName":"Amazon S3",
                                "linkProtocol":"Amazon:AWS:S3"
                            },
                            {
                                "linkFunction":"download",
                                "linkUrl":"https://archive-testing-demo.s3-us-east-2.amazonaws.com/public/NESDIS/CSB/csv/2019/12/01/20191201_08d5538c6f8dbefd7d82929623a34385_pointData.csv",
                                "linkName":"Amazon S3",
                                "linkProtocol":"HTTPS"
                            }
                        ],
                        "internalParentIdentifier":"fdb56230-87f4-49f2-ab83-104cfd073177",
                        "filesize":63751,
                        "title":"20191201_08d5538c6f8dbefd7d82929623a34385_pointData.csv"
                    },
                    "id":"77b11a1e-1b75-46e1-b7d6-99b5022ed113",
                    "type":"granule"
                }
            ],
            "meta":{
                "took":1,
                "total":6,
                "exactCount":True
            }
        }
        return MockResponse(onestop_search_response, 200)


    def mocked_search_response_data_empty(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        print ("args: "+str(args)+" kwargs: "+str(kwargs))
        onestop_search_response = {
            "data":[],
            "meta":{
                "took":1,
                "total":6,
                "exactCount":True
            }
        }
        return MockResponse(onestop_search_response, 200)

    @mock_sqs
    @mock.patch('requests.get', side_effect=mocked_search_response_data, autospec=True)
    @patch('onestop.WebPublisher')
    def test_delete_handler_happy(self, mock_wp, mock_response):
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect_to_resource('sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('sqs', self.region)
        message = create_delete_message(self.region, self.bucket, self.key)
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps(message)
        )

        mock_wp.search_onestop.side_effect = mock_response
        cb = create_delete_handler(mock_wp)

        self.sqs_consumer.receive_messages(sqs_queue, 1, cb)

        # Verify search and delete called once.
        mock_wp.search_onestop.assert_called_once()
        mock_wp.delete_registry.assert_called_once()

    @mock_sqs
    @mock.patch('requests.get', side_effect=mocked_search_response_data_empty, autospec=True)
    @patch('onestop.WebPublisher')
    def test_delete_handler_data_empty_ends_cb(self, mock_wp, mock_response):
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect_to_resource('sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('sqs', self.region)
        message = create_delete_message(self.region, self.bucket, self.key)
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps(message)
        )

        mock_wp.search_onestop.side_effect = mock_response
        cb = create_delete_handler(mock_wp)

        self.sqs_consumer.receive_messages(sqs_queue, 1, cb)

        # Verify search and delete called once.
        mock_wp.search_onestop.assert_called_once()
        mock_wp.delete_registry.assert_not_called()

    @mock_sqs
    @mock.patch('requests.get', side_effect=mocked_search_response_data, autospec=True)
    @patch('onestop.WebPublisher')
    def test_delete_handler_no_records_ends_cb(self, mock_wp, mock_response):
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect_to_resource('sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('sqs', self.region)
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps({"Message":'''{"Records":[]}'''})
        )

        mock_wp.search_onestop.side_effect = mock_response
        cb = create_delete_handler(mock_wp)

        self.sqs_consumer.receive_messages(sqs_queue, 1, cb)

        # Verify search and delete called once.
        mock_wp.search_onestop.assert_not_called()
        mock_wp.delete_registry.assert_not_called()

    @mock_sqs
    @mock.patch('requests.get', side_effect=mocked_search_response_data, autospec=True)
    @patch('onestop.WebPublisher')
    def test_delete_handler_eventName_not_delete_ends_cb(self, mock_wp, mock_response):
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect_to_resource('sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('sqs', self.region)
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps({"Message":'''{"Records":[{"eventName":"Unknown"}]}'''})
        )

        mock_wp.search_onestop.side_effect = mock_response
        cb = create_delete_handler(mock_wp)

        self.sqs_consumer.receive_messages(sqs_queue, 1, cb)

        # Verify search and delete called once.
        mock_wp.search_onestop.assert_not_called()
        mock_wp.delete_registry.assert_not_called()

if __name__ == '__main__':
    unittest.main()