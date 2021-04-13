import unittest
import yaml

from moto import mock_s3
from tests.utils import abspath_from_relative
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter

class S3MessageAdapterTest(unittest.TestCase):
    s3ma = None

    recs1 = \
        [{
          'eventVersion': '2.1',
          'eventSource': 'aws:s3',
          'awsRegion': 'us-east-1',
          'eventTime': '2020-11-10T00:44:20.642Z',
          'eventName': 'ObjectCreated:Put',
          'userIdentity': {'principalId': 'AWS:AIDAUDW4MV7I5RW5LQJIO'},
          'requestParameters': {'sourceIPAddress': '65.113.158.185'},
          'responseElements': {'x-amz-request-id': '7D394F43C682BB87', 'x-amz-id-2': 'k2Yn5BGg7DM5fIEAnwv5RloBFLYERjGRG3mT+JsPbdX033USr0eNObqkHiw3m3x+BQ17DD4C0ErB/VdhYt2Az01LJ4mQ/aqS'},
          's3': {'s3SchemaVersion': '1.0', 'configurationId': 'csbS3notification',
            'bucket': {'name': 'nesdis-ncei-csb-dev',
              'ownerIdentity': {'principalId': 'A3PGJENIF5D10L'},
              'arn': 'arn:aws:s3:::nesdis-ncei-csb-dev'},
            'object': {'key': 'csv/file1.csv', 'size': 1385,
              'eTag': '44d2452e8bc2c8013e9c673086fbab7a',
              'versionId': 'q6ls_7mhqUbfMsoYiQSiADnHBZQ3Fbzf',
              'sequencer': '005FA9E26498815778'}
          }
        }]

    recs2 = \
        [{
          'eventVersion': '2.1',
          'eventSource': 'aws:s3',
          'awsRegion': 'us-east-1',
          'eventTime': '2020-11-10T00:44:20.642Z',
          'eventName': 'ObjectCreated:Put',
          'userIdentity': {'principalId': 'AWS:AIDAUDW4MV7I5RW5LQJIO'},
          'requestParameters': {'sourceIPAddress': '65.113.158.185'},
          'responseElements': {'x-amz-request-id': '7D394F43C682BB87', 'x-amz-id-2': 'k2Yn5BGg7DM5fIEAnwv5RloBFLYERjGRG3mT+JsPbdX033USr0eNObqkHiw3m3x+BQ17DD4C0ErB/VdhYt2Az01LJ4mQ/aqS'},
          's3': {'s3SchemaVersion': '1.0', 'configurationId': 'csbS3notification',
            'bucket': {'name': 'nesdis-ncei-csb-dev',
              'ownerIdentity': {'principalId': 'A3PGJENIF5D10L'},
              'arn': 'arn:aws:s3:::nesdis-ncei-csb-dev'},
            'object': {'key': 'csv/file2.csv', 'size': 1386,
              'eTag': '44d2452e8bc2c8013e9c673086fbab7a',
              'versionId': 'q6ls_7mhqUbfMsoYiQSiADnHBZQ3Fbzf',
              'sequencer': '005FA9E26498815778'}
          }
        }]

    def setUp(self):
        print("Set it up!")

        with open(abspath_from_relative(__file__, "../../config/csb-data-stream-config-template.yml")) as f:
            self.stream_conf = yaml.load(f, Loader=yaml.FullLoader)
        with open(abspath_from_relative(__file__, "../../config/aws-util-config-dev.yml")) as f:
            self.cloud_conf = yaml.load(f, Loader=yaml.FullLoader)
        with open(abspath_from_relative(__file__, "../../config/credentials-template.yml")) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.s3_utils = S3Utils(self.cred['sandbox']['access_key'],
                                self.cred['sandbox']['secret_key'],
                                "DEBUG")
        self.s3ma = S3MessageAdapter(self.stream_conf['access_bucket'],
                                     self.stream_conf['type'],
                                     self.stream_conf['file_identifier_prefix'],
                                     self.stream_conf['collection_id'])

        self.region = self.cloud_conf['s3_region']
        self.bucket = self.cloud_conf['s3_bucket']

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.stream_conf['collection_id'] == None)

    @mock_s3
    def test_transform(self):
        s3 = self.s3_utils.connect('s3', self.region)
        location = {'LocationConstraint': self.region}
        bucket = 'nesdis-ncei-csb-dev'
        key = 'csv/file1.csv'
        key2 = 'csv/file2.csv'
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body="body")
        s3.put_object(Bucket=bucket, Key=key2, Body="body")

        payload = self.s3ma.transform(self.recs1)
        print(payload)

        payload = self.s3ma.transform(self.recs2)
        print(payload)
        self.assertTrue(payload!=None)

    @mock_s3
    def test_extra_parameters_constructor(self):
        testParams = {"access_bucket": "blah1",
                      "type": "blah2",
                      "file_id_prefix": "blah3",
                      "collection_id": "blah4",
                      "extra": "extra value"}
        self.assertRaises(Exception, S3MessageAdapter(**testParams))

if __name__ == '__main__':
    unittest.main()