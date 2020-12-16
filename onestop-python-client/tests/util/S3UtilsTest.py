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
        boto_client = self.su.connect("s3_resource", None)
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

    def test_s3_cross_region(self, key):
        print('Cross Region Vault Upload ------------- ')

        # grabs te region and bucket name from the config file
        region = self.su.conf['region']
        bucket = self.su.conf['s3_bucket']

        # makes connection to low level s3 client
        s3 = self.su.connect('s3', region)

        # Reads object data and stores it into a variable
        file_data = self.su.read_bytes_s3(s3, bucket, key)

        # Redirecting upload to vault in second region
        glacier = self.su.connect("glacier", self.su.conf['region2'])
        vault_name = self.su.conf['vault_name2']
        print('vault name: ' + str(vault_name))
        print('region name: ' + str(self.su.conf['region2']))
        print('-------file data---------')
        print(file_data)
        response = self.su.upload_archive(glacier, vault_name, file_data)

        self.assertTrue(response['location']!=None)


    def test_s3_to_glacier(self, key):
        """
        Changes the storage class of an object from S3 to Glacier
        Requires the configure and credential locations as parameters as well as the key of the object
        """

        print("S3 to Glacier---------")

        # grabs te region and bucket name from the config file
        region = self.su.conf['region']
        bucket = self.su.conf['s3_bucket']

        # Create boto3 low level api connection
        s3 = self.su.connect('s3', region)

        # Using the S3 util class invoke the change of storage class
        response = self.su.s3_to_glacier(s3, bucket, key)

        self.assertTrue(response != None)

    def test_s3_restore(self, key):
        """
        Uses high level api to restore object from glacier to s3
        """

        region = self.su.conf['region']
        bucket = self.su.conf['s3_bucket']

        days = 3

        # use high level api
        s3 = self.su.connect('s3_resource', region)


        self.assertTrue(self.su.s3_restore(s3, bucket, key, days) != None)


    def test_retrieve_inventory(self):
        """
        Initiates job for archive retrieval. Takes 3-5 hours to complete
        """

        # Using glacier api initiates job and returns archive results
        # Connect to your glacier vault for retrieval
        glacier = self.su.connect("glacier", self.su.conf['region'])
        vault_name = self.su.conf['vault_name']


        response = self.su.retrieve_inventory(glacier, vault_name)
        self.assertTrue(response['jobId']!= None)

    def test_retrieve_inventory_results(self, jobid):
        """
        Once the job has been completed, use the job id to retrieve archive results
        """

        # Connect to your glacier vault for retrieval
        glacier = self.su.connect("glacier", self.su.conf['region'])
        vault_name = self.su.conf['vault_name']

        # Retrieve the job results
        inventory = self.su.retrieve_inventory_results(vault_name, glacier, jobid)

        self.assertTrue(inventory != None)




if __name__ == '__main__':
    unittest.main()