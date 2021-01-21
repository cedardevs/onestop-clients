import logging
import yaml
import uuid
import boto3
import botocore
import json
from smart_open import open as sm_open
from botocore.exceptions import ClientError
from onestop.util.ClientLogger import ClientLogger


class S3Utils:
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def connect(self, client_type, region):

        if client_type == "s3":
            boto = boto3.client("s3", aws_access_key_id=self.cred['sandbox']['access_key'],
                                       aws_secret_access_key=self.cred['sandbox']['secret_key'], region_name=region)

        if client_type == "s3_resource":
            boto = boto3.resource("s3", region_name=region, aws_access_key_id=self.cred['sandbox']['access_key'],
                                         aws_secret_access_key=self.cred['sandbox']['secret_key'] )

        if client_type == "glacier":
            boto = boto3.client("glacier", region_name=region, aws_access_key_id=self.cred['sandbox']['access_key'],
                                       aws_secret_access_key=self.cred['sandbox']['secret_key'])

        if client_type == "session":
            boto = boto3.Session(
                aws_access_key_id=self.cred['sandbox']['access_key'],
                aws_secret_access_key=self.cred['sandbox']['secret_key'],
            )
        return boto

    def objectkey_exists(self, bucket, s3_key):
        exists = True
        try:
            s3 = boto3.resource('s3')
            s3object = s3.Object(bucket, s3_key)
            s3object.load()
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
        return exists

    def get_uuid_metadata(self, boto_client, bucket, s3_key):
        obj_uuid = None
        self.logger.debug("Get metadata")
        s3_object = boto_client.Object(bucket, s3_key)

        self.logger.info("bucket: " + bucket)
        self.logger.info("key: " + s3_key)

        s3_metadata = s3_object.metadata
        print(s3_metadata)
        if 'object-uuid' in s3_metadata:
            self.logger.info("object-uuid: " + s3_metadata['object-uuid'])
            obj_uuid = s3_metadata['object-uuid']
        return obj_uuid

    def add_uuid_metadata(self, boto_client, bucket, s3_key):
        self.logger.info("Adding uuid to object metadata")
        obj_uuid = str(uuid.uuid4())
        s3_object = boto_client.Object(bucket, s3_key)
        s3_object.metadata.update({'object-uuid': obj_uuid})
        s3_object.copy_from(
            CopySource={'Bucket': bucket, 'Key': s3_key},
            Metadata=s3_object.metadata, MetadataDirective='REPLACE' )
        return True

    def upload_s3(self, boto_client, local_file, bucket, s3_key, overwrite):
        self.logger.debug("Receive messages")

        key_exists = False
        obj_uuid = str(uuid.uuid4())

        if not overwrite:
            key_exists = self.objectkey_exists(boto_client, bucket, s3_key)

        if (not key_exists) or (key_exists and overwrite):
            try:
                boto_client.upload_file(local_file, bucket, s3_key,
                                        ExtraArgs={'Metadata': {'object-uuid': obj_uuid}})
                print("Upload successful.")
                return True
            except FileNotFoundError:
                print("The file was not found")
                return False

    def read_csv_s3(self, boto_client, bucket, key):
        url = "s3://" + bucket + "/" + key
        for line in sm_open(url, 'rb', transport_params={'session': boto_client}):
            print("reading csv:" + line.decode('utf-8'))
        return True

    def read_bytes_s3(self, boto_client, bucket, key):
        # Create a file object using the bucket and object key.
        fileobj = boto_client.get_object(
            Bucket=bucket,
            Key=key
        )
        # open the file object and read it into the variable filedata.
        filedata = fileobj['Body'].read()
        return filedata

    def upload_archive(self, boto_client, vault_name, src_data):
        """Add an archive to an Amazon S3 Glacier vault.

        The upload occurs synchronously.

        :param vault_name: string
        :param src_data: bytes of data or string reference to file spec
        :return: If src_data was added to vault, return dict of archive
        information, otherwise None
        """

        # The src_data argument must be of type bytes or string
        # Construct body= parameter
        if isinstance(src_data, bytes):
            object_data = src_data
        elif isinstance(src_data, str):
            try:
                object_data = open(src_data, 'rb')
                # possible FileNotFoundError/IOError exception
            except Exception as e:
                logging.error(e)
                return None
        else:
            logging.error('Type of ' + str(type(src_data)) +
                          ' for the argument \'src_data\' is not supported.')
            return None

        try:
            archive = boto_client.upload_archive(vaultName=vault_name,
                                                 body=object_data)
        except ClientError as e:
            logging.error(e)
            return None
        finally:
            if isinstance(src_data, str):
                object_data.close()

        # Return dictionary of archive information
        print('Archive: ' + str(archive))
        return archive

    def s3_to_glacier(self, boto_client, bucket_name, key):
        # reads the file data in s3 and store into variable to pass into put_object
        filedata = self.read_bytes_s3(boto_client, bucket_name, key)

        response = boto_client.put_object(Body=filedata, Bucket= bucket_name,StorageClass='GLACIER', Key=key)
        print(response)
        return response

    def s3_to_glacier_object_lock(self, boto_client, bucket_name, key, object_lock_mode, object_lock_retention):
        # reads the file data in s3 and store into variable to pass into put_object
        filedata = self.read_bytes_s3(boto_client,bucket_name,key)

        response = boto_client.put_object(Body=filedata, Bucket= bucket_name,StorageClass='GLACIER', Key=key, ObjectLockMode = object_lock_mode, ObjectLockRetainUntilDate=object_lock_retention)
        print(response)
        return response

    def s3_restore(self, boto_client, bucket_name, key, days):
        # Restores an object in glacier back to s3

        # create bucket object
        obj = boto_client.Object(bucket_name, key)

        # Days refers to lifetime of the active copy in days
        restore_request = {'Days': days}

        # restores the object
        obj.restore_object(RestoreRequest=restore_request)

        # returns status of object retrieval
        return obj.restore


    def retrieve_inventory(self, boto_client, vault_name):
        """Initiate an Amazon Glacier inventory-retrieval job

        To check the status of the job, call Glacier.Client.describe_job()
        To retrieve the output of the job, call Glacier.Client.get_job_output()

        :param vault_name: string
        :return: Dictionary of information related to the initiated job. If error,
        returns None.
        """

        # Construct job parameters
        job_parms = {'Type': 'inventory-retrieval'}

        try:
            response = boto_client.initiate_job(vaultName=vault_name,
                                            jobParameters=job_parms)
        except ClientError as e:
            logging.error(e)
            return None
        print('Retrieval Response: ', response)
        return response

    def retrieve_inventory_results(self, vault_name, boto_client, job_id):
        """Retrieve the results of an Amazon Glacier inventory-retrieval job

        :param vault_name: string
        :param job_id: string. The job ID was returned by Glacier.Client.initiate_job()
        :return: Dictionary containing the results of the inventory-retrieval job.
        If error, return None.
        """

        try:
            response = boto_client.get_job_output(vaultName=vault_name, jobId=job_id)
        except ClientError as e:
            logging.error(e)
            return None

        # Read the streaming results into a dictionary
        return json.loads(response['body'].read())
