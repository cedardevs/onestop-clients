import csv
import unittest
import uuid
from moto import mock_s3
from moto import mock_glacier

from tests.utils import abspath_from_relative
from onestop.util.S3Utils import S3Utils

class S3UtilsTest(unittest.TestCase):
    su = None

    def setUp(self):
        print("Set it up!")
        self.su = S3Utils(abspath_from_relative(__file__, "../../config/aws-util-config-dev.yml"),
                          abspath_from_relative(__file__, "../../config/credentials.yml"))

    def tearDown(self):
        print("Tear it down!")
        # Remove files from bucket

    def test_parse_config(self):
        self.assertFalse(self.su.conf['sqs_url']==None)

    @mock_s3
    def test_get_uuid_metadata(self):
        boto_client = self.su.connect("s3_resource", None)
        s3_key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']
        region = self.su.conf['s3_region']
        location = {'LocationConstraint': region}
        boto_client.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        obj_uuid = str(uuid.uuid4())
        boto_client.Object(bucket, s3_key).put(Bucket=bucket, Key=s3_key, Body="my_body", Metadata={'object-uuid': obj_uuid})

        self.assertFalse(self.su.get_uuid_metadata(boto_client, bucket, s3_key) == None)

    @mock_s3
    def test_add_uuid_metadata(self):
        region = self.su.conf['s3_region']
        boto_client = self.su.connect("s3_resource", region)

        s3_key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']

        location = {'LocationConstraint': region}
        boto_client.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        boto_client.Object(bucket, s3_key).put(Bucket=bucket, Key=s3_key, Body="my_body")

        self.assertTrue(self.su.add_uuid_metadata(boto_client, bucket, s3_key))

    @mock_s3
    def test_add_file_s3(self):
        boto_client = self.su.connect("s3", None)
        local_file = abspath_from_relative(__file__, "../data/file4.csv")
        s3_key = "csv/file4.csv"
        bucket = self.su.conf['s3_bucket']
        region = self.su.conf['s3_region']
        location = {'LocationConstraint': region}
        boto_client.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        overwrite = True

        self.assertTrue(self.su.upload_s3(boto_client, local_file, bucket, s3_key, overwrite))

    def test_get_csv_s3(self):
        boto_client = self.su.connect("session", None)
        s3_key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']
        sm_open_file = self.su.get_csv_s3(boto_client, bucket, s3_key)

        # print("reading csv:" + line.decode('utf-8'))
        csv_reader = csv.DictReader(sm_open_file)
        for row in csv_reader:
            print(str(row["LON"]))

    def test_read_bytes_s3(self):
        boto_client = self.su.connect("s3", None)
        s3_key = "csv/file1.csv"
        bucket = self.su.conf['s3_bucket']
        self.assertTrue(self.su.read_bytes_s3(boto_client, bucket, s3_key))

    @mock_s3
    def test_add_files(self):
        boto_client = self.su.connect("s3", None)
        local_files = ["file1_s3.csv", "file2.csv", "file3.csv"]
        bucket = self.su.conf['s3_bucket']
        region = self.su.conf['s3_region']
        location = {'LocationConstraint': region}
        boto_client.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        overwrite = True
        s3_file = None
        for file in local_files:
            local_file = abspath_from_relative(__file__, "../data/" + file)
            s3_file = "csv/" + file
            self.assertTrue(self.su.upload_s3(boto_client, local_file, bucket, s3_file, overwrite))

    @mock_s3
    @mock_glacier
    def test_s3_cross_region(self):
        print('Cross Region Vault Upload ------------- ')
        key = "csv/file1.csv"
        # grabs te region and bucket name from the config file
        region = self.su.conf['s3_region']
        bucket = self.su.conf['s3_bucket']

        # makes connection to low level s3 client
        s3 = self.su.connect('s3', region)
        location = {'LocationConstraint': region}
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body="body")

        # Reads object data and stores it into a variable
        file_data = self.su.read_bytes_s3(s3, bucket, key)

        # Redirecting upload to vault in second region
        glacier = self.su.connect("glacier", self.su.conf['s3_region2'])
        vault_name = self.su.conf['vault_name']
        glacier.create_vault(vaultName=vault_name)
        print('vault name: ' + str(vault_name))
        print('region name: ' + str(self.su.conf['s3_region2']))
        print('-------file data---------')
        print(file_data)
        response = self.su.upload_archive(glacier, vault_name, file_data)

        self.assertTrue(response['archiveId']!=None)

    @mock_s3
    @mock_glacier
    def test_s3_to_glacier(self):
        """
        Changes the storage class of an object from S3 to Glacier
        Requires the configure and credential locations as parameters as well as the key of the object
        """

        print("S3 to Glacier---------")
        key = "csv/file1_s3.csv"
        # grabs te region and bucket name from the config file
        region = self.su.conf['s3_region']
        bucket = self.su.conf['s3_bucket']

        # Create boto3 low level api connection
        s3 = self.su.connect('s3', region)
        location = {'LocationConstraint': region}
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=bucket, Key=key, Body="body")

        # Using the S3 util class invoke the change of storage class
        response = self.su.s3_to_glacier(s3, bucket, key)
        print(response['ResponseMetadata']['HTTPHeaders']['x-amz-storage-class'])
        # Assert 'x-amz-storage-class': 'GLACIER'

        self.assertTrue(response['ResponseMetadata']['HTTPHeaders']['x-amz-storage-class'] == "GLACIER")

    @mock_s3
    def test_s3_restore(self):
        """
        Uses high level api to restore object from glacier to s3
        """

        region = self.su.conf['s3_region2']
        bucket = self.su.conf['s3_bucket']
        key = "csv/file1_s3.csv"
        days = 3

        # use high level api
        s3 = self.su.connect('s3_resource', region)
        location = {'LocationConstraint': region}
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
        s3.Object(bucket, key).put(Bucket=bucket, Key=key, Body="body")

        self.assertTrue(self.su.s3_restore(s3, bucket, key, days) != None)

    @mock_glacier
    def test_retrieve_inventory(self):
        """
        Initiates job for archive retrieval. Takes 3-5 hours to complete
        """

        # Using glacier api initiates job and returns archive results
        # Connect to your glacier vault for retrieval
        glacier = self.su.connect("glacier", self.su.conf['s3_region2'])
        vault_name = self.su.conf['vault_name']
        glacier.create_vault(vaultName=vault_name)


        response = self.su.retrieve_inventory(glacier, vault_name)
        self.assertTrue(response['jobId']!= None)

    '''
    Excluding for now because it's an asynchronous test
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
    '''



if __name__ == '__main__':
    unittest.main()