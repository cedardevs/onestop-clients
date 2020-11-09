import unittest

from onestop.util.S3Utils import S3Utils

class S3UtilsTest(unittest.TestCase):
    su = None

    def setUp(self):
        print("Set it up!")
        self.su = S3Utils("../../config/aws-util-config-dev.yml", "../../config/aws-credentials.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.su.conf['sqs_url']==None)

    def test_get_uuid_metadata(self):
        boto_client = self.su.connect()
        s3_key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']

        self.assertTrue(self.su.get_uuid_metadata(boto_client, bucket, s3_key)=="9f0a5ff2-fcc0-5bcb-a225-024b669c9bba")


    def test_upload(self):
        boto_client = self.su.connect()
        local_file = "../data/file1.csv"
        s3_file = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']
        overwrite = True

        self.assertTrue(self.su.upload_file(boto_client, local_file, bucket, s3_file, overwrite))

    def test_uploads(self):
        boto_client = self.su.connect()
        local_files = ["file1.csv", "file2.csv", "file3.csv"]
        bucket = self.su.conf['s3_bucket']
        overwrite = True
        s3_file = None
        for file in local_files:
            local_file = "../data/" + file
            s3_file = "csv/" + file
            self.assertTrue(self.su.upload_file(boto_client, local_file, bucket, s3_file, overwrite))

if __name__ == '__main__':
    unittest.main()