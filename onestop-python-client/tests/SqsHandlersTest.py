import json
import unittest
import boto3
import yaml
from moto import mock_s3
from moto import mock_sqs
from tests.utils import abspath_from_relative, create_delete_message
from onestop.WebPublisher import WebPublisher
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.SqsHandlers import create_delete_handler


class SqsHandlerTest(unittest.TestCase):
    wp = None
    su = None
    s3ma = None
    sqs = None
    wp_config = abspath_from_relative(__file__, "../config/web-publisher-config-local.yml")
    aws_config = abspath_from_relative(__file__, "../config/aws-util-config-dev.yml")
    cred_config = abspath_from_relative(__file__, "../config/credentials-template.yml")
    csb_config = abspath_from_relative(__file__, "../config/csb-data-stream-config.yml")

    collection_uuid = '5b58de08-afef-49fb-99a1-9c5d5c003bde'
    payloadDict = {
        "fileInformation": {
            "name": "OR_ABI-L1b-RadF-M6C13_G16_s20192981730367_e20192981740087_c20192981740157.nc",
            "size": 30551050,
            "checksums": [{
                "algorithm": "SHA1",
                "value": "bf4c5b58f8d5f9445f7b277f988e5861184f775a"
            }],
            "format": "NetCDF"
        },
        "relationships": [{
            "type": "COLLECTION",
            "id": collection_uuid
        }],
        "fileLocations": {
            "s3://noaa-goes16/ABI-L1b-RadF/2019/298/17/OR_ABI-L1b-RadF-M6C13_G16_s20192981730367_e20192981740087_c20192981740157.nc": {
                "uri": "s3://noaa-goes16/ABI-L1b-RadF/2019/298/17/OR_ABI-L1b-RadF-M6C13_G16_s20192981730367_e20192981740087_c20192981740157.nc",
                "type": "ACCESS",
                "deleted": "false",
                "restricted": "false",
                "asynchronous": "false",
                "locality": "us-east-2",
                "lastModified": 1572025823000,
                "serviceType": "Amazon:AWS:S3",
                "optionalAttributes": {}
            }
        }
    }

    def setUp(self):
        print("Set it up!")

        with open(abspath_from_relative(__file__, "../config/csb-data-stream-config-template.yml")) as f:
            self.stream_conf = yaml.load(f, Loader=yaml.FullLoader)
        with open(abspath_from_relative(__file__, "../config/aws-util-config-dev.yml")) as f:
            self.cloud_conf = yaml.load(f, Loader=yaml.FullLoader)
        with open(abspath_from_relative(__file__, "../config/credentials-template.yml")) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.wp = WebPublisher(self.wp_config, self.cred_config)
        self.su = S3Utils(self.cred['sandbox']['access_key'],
                          self.cred['sandbox']['secret_key'],
                          "DEBUG")
        self.s3ma = S3MessageAdapter(self.stream_conf['access_bucket'],
                                     self.stream_conf['type'],
                                     self.stream_conf['file_identifier_prefix'],
                                     self.stream_conf['collection_id'])

    def tearDown(self):
        print("Tear it down!")

    @mock_s3
    @mock_sqs
    def init_s3(self):
        bucket = self.cloud_conf['s3_bucket']
        key = self.cloud_conf['s3_key']
        boto_client = self.su.connect("s3", None)
        boto_client.create_bucket(Bucket=bucket)
        boto_client.put_object(Bucket=bucket, Key=key, Body="foobar")

        sqs_client = boto3.client('sqs', region_name=self.cloud_conf['s3_region'])
        sqs_queue = sqs_client.create_queue(QueueName=self.cloud_conf['sqs_name'])
        self.sqs = SqsConsumer(self.aws_config, self.cred_config)
        message = create_delete_message(self.cloud_conf['s3_region'], bucket, key)
        sqs_client.send_message(QueueUrl=sqs_queue['QueueUrl'], MessageBody=json.dumps(message))
        sqs_queue['QueueUrl']

    @mock_s3
    @mock_sqs
    def delete_handler_wrapper(self, recs):
        handler = create_delete_handler(self.wp)
        result = handler(recs)
        self.assertTrue(result)

    @mock_sqs
    def test_delete_handler(self):
        mock_queue_url = self.init_s3()
        sqs_queue = boto3.resource('sqs', region_name=self.stream_conf['s3_region']).Queue(mock_queue_url)
        self.sqs.receive_messages(sqs_queue, self.stream_conf['sqs_max_polls'], self.delete_handler_wrapper)

if __name__ == '__main__':
    unittest.main()