import unittest

from onestop.util.S3MessageAdapter import S3MessageAdapter


class S3MessageAdapterTest(unittest.TestCase):
    s3ma = None
    recs = \
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
            'object': {'key': 'csv/file2.csv', 'size': 1385,
              'eTag': '44d2452e8bc2c8013e9c673086fbab7a',
              'versionId': 'q6ls_7mhqUbfMsoYiQSiADnHBZQ3Fbzf',
              'sequencer': '005FA9E26498815778'}
          }
        }]

    def setUp(self):
        print("Set it up!")
        self.s3ma = S3MessageAdapter("../../config/csb-data-stream-config.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.s3ma.conf['collection_id']==None)

    def test_transform(self):
        payload = self.s3ma.transform(self.recs)
        self.assertTrue(payload!=None)

if __name__ == '__main__':
    unittest.main()