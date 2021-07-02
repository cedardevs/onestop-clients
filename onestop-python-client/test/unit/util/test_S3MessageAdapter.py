import unittest

from onestop.util.S3MessageAdapter import S3MessageAdapter

class S3MessageAdapterTest(unittest.TestCase):
    config_dict = {
        'access_key': 'test_access_key',
        'secret_key': 'test_secret_key',
        'access_bucket': 'https://archive-testing-demo.s3-us-east-2.amazonaws.com',
        's3_message_adapter_metadata_type': 'COLLECTION',
        'file_id_prefix': 'gov.noaa.ncei.csb:',
        'collection_id': 'fdb56230-87f4-49f2-ab83-104cfd073177',
        'log_level': 'DEBUG'
    }

    recs_minimum_fields = \
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

    def test_init_metadata_type_valid(self):
        publisher = S3MessageAdapter(**self.config_dict)

        self.assertEqual(publisher.metadata_type, self.config_dict['s3_message_adapter_metadata_type'])

    def test_init_metadata_type_invalid(self):
        wrong_metadata_type_config = dict(self.config_dict)
        wrong_metadata_type_config['s3_message_adapter_metadata_type'] = "invalid_type"

        self.assertRaises(ValueError, S3MessageAdapter, **wrong_metadata_type_config)

    def test_init_metadata_type_lowercase(self):
        metadata_type = 'collection'
        uppercase_metadata_type = metadata_type.upper()
        config = dict(self.config_dict)
        config['s3_message_adapter_metadata_type'] = metadata_type

        s3MA = S3MessageAdapter(**config)

        self.assertEqual(uppercase_metadata_type, s3MA.metadata_type)

    def test_init_extra_parameters_constructor(self):
        test_params = dict(self.config_dict)
        test_params['extra'] = 'extra value'
        self.assertRaises(Exception, S3MessageAdapter(**test_params))

    def test_transform(self):
        s3MA = S3MessageAdapter(**self.config_dict)
        payload = s3MA.transform(self.recs_minimum_fields)

        self.assertIsNotNone(payload)


if __name__ == '__main__':
    unittest.main()