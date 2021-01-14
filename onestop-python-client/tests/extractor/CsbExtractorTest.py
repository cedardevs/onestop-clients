import unittest
from moto import mock_s3
from onestop.util.S3Utils import S3Utils
from tests.utils import abspath_from_relative
from onestop.extract.CsbExtractor import CsbExtractor

class CsbExtractorTest(unittest.TestCase):
    recs1 = \
        [{
            'eventVersion': '2.1',
            'eventSource': 'aws:s3',
            'awsRegion': 'us-east-1',
            'eventTime': '2020-11-10T00:44:20.642Z',
            'eventName': 'ObjectCreated:Put',
            'userIdentity': {'principalId': 'AWS:AIDAUDW4MV7I5RW5LQJIO'},
            'requestParameters': {'sourceIPAddress': '65.113.158.185'},
            'responseElements': {'x-amz-request-id': '7D394F43C682BB87',
                                 'x-amz-id-2': 'k2Yn5BGg7DM5fIEAnwv5RloBFLYERjGRG3mT+JsPbdX033USr0eNObqkHiw3m3x+BQ17DD4C0ErB/VdhYt2Az01LJ4mQ/aqS'},
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


    def setUp(self):
        print("Set it up!")
        self.s3_utils = S3Utils(abspath_from_relative(__file__, "../../config/aws-util-config-dev.yml"),
                                abspath_from_relative(__file__, "../../config/credentials-template.yml"))
        self.csb_extractor = CsbExtractor(abspath_from_relative(__file__, "../../config/csb-data-stream-config.yml"),
                                     self.s3_utils)

    def tearDown(self):
        print("Tear it down!")

    def test_csv(self):
        key1 = self.recs1[0]['s3']['object']['key']
        csv_str= '.csv'
        self.assertTrue(key1.endswith(csv_str))

    @mock_s3
    def test_get_line(self):
        s3 = self.s3_utils.connect('s3', self.s3_utils.conf['s3_region'])
        location = {'LocationConstraint': self.s3_utils.conf['s3_region']}
        bucket = 'nesdis-ncei-csb-dev'
        key = 'csv/file4.csv'

        with open('../data/file4.csv', 'r') as file:
            data = file.read()

        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body=data)

        line = self.csb_extractor.get_line(bucket, key)

        self.assertTrue(line != None)

    @mock_s3
    def test_get_max_numeric(self):
        s3 = self.s3_utils.connect('s3', self.s3_utils.conf['s3_region'])
        location = {'LocationConstraint': self.s3_utils.conf['s3_region']}
        bucket = 'nesdis-ncei-csb-dev'
        key = 'csv/file4.csv'

        with open('../data/file4.csv', 'r') as file:
            data = file.read()

        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body=data)

        line = self.csb_extractor.get_line(bucket, key)
        max_lon = self.csb_extractor.get_max_numeric(line, 'LON')
        self.assertEqual(max_lon, -92.747995)

    @mock_s3
    def test_get_min_numeric(self):
        s3 = self.s3_utils.connect('s3', self.s3_utils.conf['s3_region'])
        location = {'LocationConstraint': self.s3_utils.conf['s3_region']}
        bucket = 'nesdis-ncei-csb-dev'
        key = 'csv/file4.csv'

        with open('../data/file4.csv', 'r') as file:
            data = file.read()

        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body=data)

        line = self.csb_extractor.get_line(bucket, key)
        min_lon = self.csb_extractor.get_min_numeric(line, 'LON')
        self.assertEqual(min_lon, -96.847995)

    @mock_s3
    def test_get_max_datetime(self):
        s3 = self.s3_utils.connect('s3', self.s3_utils.conf['s3_region'])
        location = {'LocationConstraint': self.s3_utils.conf['s3_region']}
        bucket = 'nesdis-ncei-csb-dev'
        key = 'csv/file4.csv'

        with open('../data/file4.csv', 'r') as file:
            data = file.read()

        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body=data)

        line = self.csb_extractor.get_line(bucket, key)
        end_date = self.csb_extractor.get_max_datetime(line, 'TIME')
        self.assertEqual(end_date, '2020-04-10T14:00:06.000Z')

    @mock_s3
    def test_get_min_datetime(self):
        s3 = self.s3_utils.connect('s3', self.s3_utils.conf['s3_region'])
        location = {'LocationConstraint': self.s3_utils.conf['s3_region']}
        bucket = 'nesdis-ncei-csb-dev'
        key = 'csv/file4.csv'

        with open('../data/file4.csv', 'r') as file:
            data = file.read()

        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body=data)

        line = self.csb_extractor.get_line(bucket, key)
        begin_date = self.csb_extractor.get_min_datetime(line, 'TIME')
        self.assertEqual(begin_date, '2018-04-10T14:00:06.000Z')

    @mock_s3
    def test_extract_coords(self):
        s3 = self.s3_utils.connect('s3', self.s3_utils.conf['s3_region'])
        location = {'LocationConstraint': self.s3_utils.conf['s3_region']}
        bucket = 'nesdis-ncei-csb-dev'
        key = 'csv/file4.csv'

        with open('../data/file4.csv', 'r') as file:
            data = file.read()

        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body=data)

        line = self.csb_extractor.get_line(bucket, key)
        max_lon = self.csb_extractor.get_max_numeric(line, 'LON')
        min_lon = self.csb_extractor.get_min_numeric(line, 'LON')
        max_lat = self.csb_extractor.get_max_numeric(line, 'LAT')
        min_lat = self.csb_extractor.get_min_numeric(line, 'LAT')
        coords = self.csb_extractor.extract_coords(line, max_lon, max_lat, min_lon, min_lat)
        result = [[
            -94.847995,
            29.373065
        ],
            [
                -96.847995,
                29.373065
            ],
            [
                -94.847995,
                33.373065
            ],
            [
                -92.747995,
                29.383065
            ]
        ]
        self.assertEqual(coords, result)


if __name__ == '__main__':
    unittest.main()