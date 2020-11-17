import unittest

from onestop.util.S3Utils import S3Utils

class S3UtilsTest(unittest.TestCase):
    su = None

    def setUp(self):
        print("Set it up!")
        self.su = S3Utils("../../config/aws-util-config-dev.yml", "../../config/credentials.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.su.conf['sqs_url']==None)

    def test_get_uuid_metadata(self):
        boto_client = self.su.connect("s3", None)
        s3_key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']

        self.assertFalse(self.su.get_uuid_metadata(boto_client, bucket, s3_key) == None)

    def test_add_uuid_metadata(self):
        boto_client = self.su.connect("s3_resource", None)
        s3_key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']

        self.assertTrue(self.su.add_uuid_metadata(boto_client, bucket, s3_key))

    def test_upload_s3(self):
        boto_client = self.su.connect("s3", None)
        local_file = "../data/file1.csv"
        s3_key= "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']
        overwrite = True

        self.assertTrue(self.su.upload_s3(boto_client, local_file, bucket, s3_key, overwrite))

    def test_upload_archive(self):
        key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']
        s3 = self.su.connect("s3", self.su.conf['region'])
        file_data = self.su.read_bytes_s3(s3, bucket, key)
        glacier = self.su.connect("glacier", self.su.conf['region'])
        vault_name = self.su.conf['vault_name']
        bucket = self.su.conf['s3_bucket']
        resp_dict = self.su.upload_archive(glacier, vault_name, file_data)
        #print(str(resp_dict))
        print("archiveLocation: " + resp_dict['location'])
        print("archiveId: " + resp_dict['archiveId'])
        print("sha256: " + resp_dict['checksum'])
        self.assertTrue(resp_dict['location']!=None)

    def test_uploads(self):
        boto_client = self.su.connect("s3", None)
        local_files = ["file1.csv", "file2.csv", "file3.csv"]
        bucket = self.su.conf['s3_bucket']
        overwrite = True
        s3_file = None
        for file in local_files:
            local_file = "../data/" + file
            s3_file = "csv/" + file
            self.assertTrue(self.su.upload_s3(boto_client, local_file, bucket, s3_file, overwrite))

if __name__ == '__main__':
    unittest.main()