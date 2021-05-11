import csv
import unittest
import uuid

from moto import mock_s3
from moto import mock_glacier
from tests.utils import abspath_from_relative
from onestop.util.S3Utils import S3Utils

class S3UtilsTest(unittest.TestCase):

    def setUp(self):
        print("Set it up!")

        config_dict = {
            'access_key': 'test_access_key',
            'secret_key': 'test_secret_key',
            'access_bucket': 'https://archive-testing-demo.s3-us-east-2.amazonaws.com',
            'type': 'COLLECTION',
            'file_id_prefix': 'gov.noaa.ncei.csb:',
            'collection_id': 'fdb56230-87f4-49f2-ab83-104cfd073177',
            'log_level': 'DEBUG'
        }

        self.s3_utils = S3Utils(**config_dict)

        self.region = 'us-east-2'
        self.region2 = 'eu-north-1'
        self.bucket = 'archive-testing-demo'

    @mock_s3
    def test_get_uuid_metadata(self):
        boto_client = self.s3_utils.connect('resource', 's3', None)
        s3_key = "csv/file1.csv"

        location = {'LocationConstraint': self.region}
        boto_client.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        obj_uuid = str(uuid.uuid4())
        boto_client.Object(self.bucket, s3_key).put(Bucket=self.bucket, Key=s3_key, Body="my_body", Metadata={'object-uuid': obj_uuid})

        self.assertFalse(self.s3_utils.get_uuid_metadata(boto_client, self.bucket, s3_key) == None)

    @mock_s3
    def test_add_uuid_metadata(self):
        boto_client = self.s3_utils.connect('resource', 's3', self.region)

        s3_key = "csv/file1.csv"

        location = {'LocationConstraint': self.region}
        boto_client.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        boto_client.Object(self.bucket, s3_key).put(Bucket=self.bucket, Key=s3_key, Body="my_body")

        self.assertTrue(self.s3_utils.add_uuid_metadata(boto_client, self.bucket, s3_key))

    @mock_s3
    def test_add_file_s3(self):
        boto_client = self.s3_utils.connect('client', 's3', None)
        local_file = abspath_from_relative(__file__, "../data/file4.csv")
        s3_key = "csv/file4.csv"
        location = {'LocationConstraint': self.region}
        boto_client.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        overwrite = True

        self.assertTrue(self.s3_utils.upload_s3(boto_client, local_file, self.bucket, s3_key, overwrite))

    @mock_s3
    def test_get_csv_s3(self):
        boto_session = self.s3_utils.connect('session', None, None)
        s3 = self.s3_utils.connect('client', 's3', self.region)
        location = {'LocationConstraint': self.region}
        s3_key = "csv/file1.csv"
        s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=self.bucket, Key=s3_key, Body="body")

        sm_open_file = self.s3_utils.get_csv_s3(boto_session, self.bucket, s3_key)

        # print("reading csv:" + line.decode('utf-8'))
        csv_reader = csv.DictReader(sm_open_file)
        for row in csv_reader:
            print(str(row["LON"]))

    @mock_s3
    def test_read_bytes_s3(self):
        boto_client = self.s3_utils.connect('client', 's3', None)
        s3_key = "csv/file1.csv"
        boto_client.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': self.region})
        boto_client.put_object(Bucket=self.bucket, Key=s3_key, Body="body")

        self.assertTrue(self.s3_utils.read_bytes_s3(boto_client, self.bucket, s3_key))

    @mock_s3
    def test_add_files(self):
        boto_client = self.s3_utils.connect('client', 's3', None)
        local_files = ["file1_s3.csv", "file2.csv", "file3.csv"]
        location = {'LocationConstraint': self.region}
        boto_client.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        overwrite = True

        for file in local_files:
            local_file = abspath_from_relative(__file__, "../data/" + file)
            s3_file = "csv/" + file
            self.assertTrue(self.s3_utils.upload_s3(boto_client, local_file, self.bucket, s3_file, overwrite))

    @mock_s3
    @mock_glacier
    def test_s3_cross_region(self):
        print('Cross Region Vault Upload ------------- ')
        key = "csv/file1.csv"

        # makes connection to low level s3 client
        s3 = self.s3_utils.connect('client', 's3', self.region)
        location = {'LocationConstraint': self.region}
        s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=self.bucket, Key=key, Body="body")

        # Reads object data and stores it into a variable
        file_data = self.s3_utils.read_bytes_s3(s3, self.bucket, key)

        # Redirecting upload to vault in second region
        glacier = self.s3_utils.connect('client', 'glacier', self.region2)
        vault_name = 'archive-vault-new'
        glacier.create_vault(vaultName=vault_name)
        print('vault name: ' + str(vault_name))
        print('region name: ' + str(self.region2))
        print('-------file data---------')
        print(file_data)
        response = self.s3_utils.upload_archive(glacier, vault_name, file_data)

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

        # Create boto3 low level api connection
        s3 = self.s3_utils.connect('client', 's3', self.region)
        location = {'LocationConstraint': self.region}
        s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        s3.put_object(Bucket=self.bucket, Key=key, Body="body")

        # Using the S3 util class invoke the change of storage class
        response = self.s3_utils.s3_to_glacier(s3, self.bucket, key)
        print(response['ResponseMetadata']['HTTPHeaders']['x-amz-storage-class'])
        # Assert 'x-amz-storage-class': 'GLACIER'

        self.assertTrue(response['ResponseMetadata']['HTTPHeaders']['x-amz-storage-class'] == "GLACIER")

    @mock_s3
    def test_s3_restore(self):
        """
        Uses high level api to restore object from glacier to s3
        """

        key = "csv/file1_s3.csv"
        days = 3

        # use high level api
        s3 = self.s3_utils.connect('resource', 's3' , self.region2)
        location = {'LocationConstraint': self.region2}
        s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration=location)
        s3.Object(self.bucket, key).put(Bucket=self.bucket, Key=key, Body="body")

        self.assertTrue(self.s3_utils.s3_restore(s3, self.bucket, key, days) != None)

    @mock_glacier
    def test_retrieve_inventory(self):
        """
        Initiates job for archive retrieval. Takes 3-5 hours to complete if not mocked.
        """

        # Using glacier api initiates job and returns archive results
        # Connect to your glacier vault for retrieval
        glacier = self.s3_utils.connect('client', 'glacier', self.region2)
        vault_name = 'archive-vault-new'
        glacier.create_vault(vaultName=vault_name)


        response = self.s3_utils.retrieve_inventory(glacier, vault_name)
        self.assertTrue(response['jobId']!= None)

    '''
    Excluding for now because it's an asynchronous test
    def test_retrieve_inventory_results(self, jobid):
        """
        Once the job has been completed, use the job id to retrieve archive results
        """

        # Connect to your glacier vault for retrieval
        glacier = self.su.connect('client', 'glacier', self.su.conf['region'])
        vault_name = self.su.conf['vault_name']

        # Retrieve the job results
        inventory = self.su.retrieve_inventory_results(vault_name, glacier, jobid)

        self.assertTrue(inventory != None)
    '''

    @mock_s3
    def test_extra_parameters_constructor(self):
        testParams = {"access_key": "blah",
                      "secret_key": "blah",
                      "log_level": "DEBUG",
                      "extra": "extra value"}
        self.assertRaises(Exception, S3Utils(**testParams))

if __name__ == '__main__':
    unittest.main()