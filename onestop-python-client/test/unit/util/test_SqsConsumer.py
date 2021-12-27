import unittest
import json

from moto import mock_sqs
from unittest.mock import MagicMock, ANY
from onestop.util.S3Utils import S3Utils
from onestop.util.SqsConsumer import SqsConsumer

class SqsConsumerTest(unittest.TestCase):
    config_dict = {
        'access_key': 'test_access_key',
        'secret_key': 'test_secret_key',
        's3_region': 'us-east-2',
        's3_bucket': 'archive-testing-demo',
        'sqs_url': 'https://sqs.us-east-2.amazonaws.com/798276211865/cloud-archive-client-sqs',
        'metadata_type': 'COLLECTION',
        'file_id_prefix': 'gov.noaa.ncei.csb:',
        'collection_id': 'fdb56230-87f4-49f2-ab83-104cfd073177',
        'registry_base_url': 'http://localhost/onestop/api/registry',
        'registry_username': 'admin',
        'registry_password': 'whoknows',
        'onestop_base_url': 'http://localhost/onestop/api/search/search',
        'log_level': 'DEBUG'
    }

    records = [{"eventVersion":"2.1"}]
    message = json.dumps(
        {"Type": "Notification",
         "MessageId": "9d0691d2-ae9c-58f9-a9f4-c8dcf05d87be",
         "TopicArn": "arn:aws:sns:us-east-1:798276211865:archive-testing-demo-backup-use-1",
         "Subject": "Amazon S3 Notification",
         "Message": json.dumps({"Records": records}),
         "Timestamp": "2021-05-06T21:15:45.427Z",
         "SignatureVersion": "1",
         "Signature": "Ui5s4uVgcMr5fjGmePCMgmi14Dx9oS8hIpjXXiQo+xZPgsHkUayz7dEeGmMGGt45l8blmZTZEbxJG+HVGfIUmQGRqoimwiLm+mIAaNIN/BV76FVFcQUIkORX8gYN0a4RS3HU8/ElrKFK8Iz0zpxJdjwxa3xPCDwu+dTotiLTJxSouvg8MmkkDnq758a8vZ9WK2PaOlZiZ3m8Mv2ZvLrozZ/DAAz48HSad6Mymhit82RpGCUxy4SDwXVlP/nLB01AS11Gp2HowJR8NXyStrZYzzQEc+PebITaExyikgTMiVhRHkmb7JrtZPpgZu2daQsSooqpwyIzb6pvgwu9W54jkw==",
         "SigningCertURL": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
         "UnsubscribeURL": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:798276211865:archive-testing-demo-backup-use-1:e7a9a9f5-792e-48a6-9ec8-40f7f5a8f600"
         })

    message_wo_records = json.dumps(
        {"Type": "Notification",
         "MessageId": "9d0691d2-ae9c-58f9-a9f4-c8dcf05d87be",
         "TopicArn": "arn:aws:sns:us-east-1:798276211865:archive-testing-demo-backup-use-1",
         "Subject": "Amazon S3 Notification",
         "Message": "{}",
         "Timestamp": "2021-05-06T21:15:45.427Z",
         "SignatureVersion": "1",
         "Signature": "Ui5s4uVgcMr5fjGmePCMgmi14Dx9oS8hIpjXXiQo+xZPgsHkUayz7dEeGmMGGt45l8blmZTZEbxJG+HVGfIUmQGRqoimwiLm+mIAaNIN/BV76FVFcQUIkORX8gYN0a4RS3HU8/ElrKFK8Iz0zpxJdjwxa3xPCDwu+dTotiLTJxSouvg8MmkkDnq758a8vZ9WK2PaOlZiZ3m8Mv2ZvLrozZ/DAAz48HSad6Mymhit82RpGCUxy4SDwXVlP/nLB01AS11Gp2HowJR8NXyStrZYzzQEc+PebITaExyikgTMiVhRHkmb7JrtZPpgZu2daQsSooqpwyIzb6pvgwu9W54jkw==",
         "SigningCertURL": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
         "UnsubscribeURL": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:798276211865:archive-testing-demo-backup-use-1:e7a9a9f5-792e-48a6-9ec8-40f7f5a8f600"
         })

    @mock_sqs
    def setUp(self):
        print("Set it up!")

        self.s3_utils = S3Utils(**self.config_dict)
        self.sqs_consumer = SqsConsumer(**self.config_dict)

    def tearDown(self):
        print("Tear it down!")

    @mock_sqs
    def test_connect(self):
        queue_name = 'test'
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.config_dict['s3_region'])
        expQueue = sqs_resource.create_queue(QueueName=queue_name)
        queue = self.sqs_consumer.connect(sqs_resource, queue_name)

        self.assertEqual(expQueue.url, queue.url)

    # Kind of pointless since we catch every exception this doesn't fail when it should....
    @mock_sqs
    def test_receive_messages_no_records(self):
        mock_cb = MagicMock()

        # Create the mock queue beforehand and set SqsConsumer's 'sqs_url' to the mock's URL
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.config_dict['s3_region'])
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url

        # Send a test message lacking Records field
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.config_dict['s3_region'])
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody= self.message_wo_records
        )
        queue = sqs_resource.Queue(queue_name)

        self.sqs_consumer.receive_messages(queue, 1, mock_cb)

        # Verify callback function was called once with expected message attributes
        mock_cb.assert_not_called()

    @mock_sqs
    def test_receive_messages_fails_invalid_sqs_max_polls(self):
        with self.assertRaises(ValueError):
            self.sqs_consumer.receive_messages(MagicMock(), 0, MagicMock())

    @mock_sqs
    def test_receive_messages_polls_msgs_expected_times(self):
        mock_cb = MagicMock()
        queue = MagicMock()

        sqs_max_polls = 2
        self.sqs_consumer.receive_messages(queue, sqs_max_polls, mock_cb)

        # Verify polling called expected times
        self.assertEqual(queue.receive_messages.call_count, sqs_max_polls)

    @mock_sqs
    def test_receive_messages_callback_occurs(self):
        mock_cb = MagicMock()

        # Create the mock queue beforehand and set SqsConsumer's 'sqs_url' to the mock's URL
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.config_dict['s3_region'])
        sqs_queue_url = sqs_resource.create_queue(QueueName=queue_name).url

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.config_dict['s3_region'])
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody= self.message
        )
        queue = sqs_resource.Queue(queue_name)

        self.sqs_consumer.receive_messages(queue, 1, mock_cb)

        # Verify callback function was called once with expected message attributes
        mock_cb.assert_called_with(self.records[0], ANY)

    @mock_sqs
    def test_happy_path(self):
        mock_cb = MagicMock()

        # Create the mock queue beforehand and set SqsConsumer's 'sqs_url' to the mock's URL
        queue_name = 'test_queue'
        sqs_resource = self.s3_utils.connect('resource', 'sqs', self.config_dict['s3_region'])
        queue = self.sqs_consumer.connect(sqs_resource, queue_name) #sqs_resource.create_queue(QueueName=queue_name)

        # Send a test message
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.config_dict['s3_region'])
        sqs_client.send_message(
            QueueUrl=queue.url,
            MessageBody= self.message
        )

        self.sqs_consumer.receive_messages(queue, 1, mock_cb)

        # Verify callback function was called once with expected message attributes
        mock_cb.assert_called_with(self.records[0], ANY)

    # An example using external send/receive methods
    @unittest.skip
    @mock_sqs
    def test_write_message_valid(self):
        "Test the write_message method with a valid message"
        sqs_client = self.s3_utils.connect('client', 'sqs' , self.config_dict['s3_region'])
        sqs = self.s3_utils.connect('resource', 'sqs', self.config_dict['s3_region'])
        queue = sqs.create_queue(QueueName='test-skype-sender')
        self.sqs_consumer.sqs_url = queue.url
        skype_message = 'Testing with a valid message'
        channel = 'test'
        expected_message = str({'msg':f'{skype_message}', 'channel':channel})
        message = str({'msg':f'{skype_message}', 'channel':channel})
        queue.send_message(MessageBody=(message))

        sqs_messages = queue.receive_messages()
        print('Message: %s'%sqs_messages)
        print('Message0: %s'%sqs_messages[0])
        assert sqs_messages[0].body == expected_message, 'Message in skype-sender does not match expected'
        print(f'The message in skype-sender SQS matches what we sent')
        assert len(sqs_messages) == 1, 'Expected exactly one message in SQS'
        print(f'\nExactly one message in skype-sender SQS')

if __name__ == '__main__':
    unittest.main()