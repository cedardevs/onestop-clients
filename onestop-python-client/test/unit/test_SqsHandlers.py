import json
import unittest

from unittest import mock
from unittest.mock import patch
from moto import mock_sqs
from test.utils import abspath_from_relative, create_delete_message
from onestop.WebPublisher import WebPublisher
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.SqsHandlers import create_delete_handler
from onestop.util.SqsHandlers import create_upload_handler
from onestop.schemas.util.jsonEncoder import EnumEncoder

class test_SqsHandler(unittest.TestCase):

    def setUp(self):
        print("Set it up!")

        self.config_dict = {
            'access_key': 'test_access_key',
            'secret_key': 'test_secret_key',
            'access_bucket': 'https://archive-testing-demo.s3-us-east-2.amazonaws.com',
            's3_message_adapter_metadata_type': 'COLLECTION',
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
        self.s3_message_adapter = S3MessageAdapter(**self.config_dict)
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
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.region)
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
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.region)
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
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.region)
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
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.region)
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

    @mock_sqs
    @patch('onestop.WebPublisher')
    @patch('onestop.util.S3Utils')
    def test_upload_handler_happy(self, mock_s3_utils, mock_wp):
        bucket = self.bucket
        key = self.key
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.region)
        message = create_delete_message(self.region, bucket, key)
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps(message)
        )

        cb = create_upload_handler(mock_wp, mock_s3_utils, self.s3_message_adapter)
        self.sqs_consumer.receive_messages(sqs_queue, 1, cb)

        # Verify get uuid called
        mock_s3_utils.connect.assert_called_with('resource', 's3', None)
        mock_s3_utils.get_uuid_metadata.assert_called_with(
            mock_s3_utils.connect(),
            bucket,
            key)
        # Verify uuid not added
        mock_s3_utils.add_uuid_metadata.assert_not_called()
        # Verify publish called & transform called
        mock_wp.publish_registry.assert_called_with(
            'granule',
            mock_s3_utils.get_uuid_metadata(),
            json.dumps(self.s3_message_adapter.transform(json.loads(message['Message'])['Records'][0]).to_dict(), cls=EnumEncoder),
            'POST'
        )

    @mock_sqs
    @patch('onestop.WebPublisher')
    @patch('onestop.util.S3Utils')
    def test_upload_handler_adds_uuid(self, mock_s3_utils, mock_wp):
        bucket = self.bucket
        key = self.key
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.region)
        message = create_delete_message(self.region, bucket, key)
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps(message)
        )

        mock_s3_utils.get_uuid_metadata.return_value = None
        cb = create_upload_handler(mock_wp, mock_s3_utils, self.s3_message_adapter)

        self.sqs_consumer.receive_messages(sqs_queue, 1, cb)

        # Verify add uuid called
        mock_s3_utils.add_uuid_metadata.assert_called_with(
            mock_s3_utils.connect(),
            bucket,
            key)

    @mock_sqs
    @patch('onestop.WebPublisher')
    @patch('onestop.util.S3Utils')
    def test_upload_handler_bucket_as_backup_PATCH(self, mock_s3_utils, mock_wp):
        bucket = "testing_backup_bucket" # backup in bucket means a PATCH should happen.
        key = self.key
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.region)
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url
        sqs_queue = sqs_resource.Queue(queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.region)
        message = create_delete_message(self.region, bucket, key)
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps(message)
        )

        cb = create_upload_handler(mock_wp, mock_s3_utils, self.s3_message_adapter)

        self.sqs_consumer.receive_messages(sqs_queue, 1, cb)

        # Verify publish called
        mock_wp.publish_registry.assert_called_with(
            'granule',
            mock_s3_utils.get_uuid_metadata(),
            json.dumps(self.s3_message_adapter.transform(json.loads(message['Message'])['Records'][0]).to_dict(), cls=EnumEncoder),
            'PATCH'
        )

if __name__ == '__main__':
    unittest.main()