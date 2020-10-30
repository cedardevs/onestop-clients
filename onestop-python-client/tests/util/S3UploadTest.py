import unittest

from onestop.util.S3Upload import S3Upload

class S3UploadTest(unittest.TestCase):
    su = None

    def setUp(self):
        print("Set it up!")
        self.su = S3Upload("../../config/aws-util-config-dev.yml", "../../config/aws-credentials.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.su.conf['sqs_url']==None)

    def test_upload(self):
        boto_client = self.su.connect()
        local_file = "/Users/dneufeld/repos/onestop-clients/onestop-python-client/tests/data/file1.csv"
        s3_file = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']
        overwrite = True
        self.su.upload_file(boto_client, local_file, bucket, s3_file, overwrite)


if __name__ == '__main__':
    unittest.main()