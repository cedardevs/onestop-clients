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
    """
    A class to utilize various AWS S3 functionalities

    Attributes
    ----------
    conf: yaml file
        aws-util-config-dev.yml
    cred: yaml file
        credentials.yml
    logger: ClientLogger object
            utilizes python logger library and creates logging for our specific needs
    logger.info: ClientLogger object
        logging statement that occurs when the class is instantiated

    Methods
    -------
    connect(client_type, region)
        connects to a boto3 client

    objectkey_exists(bucket, s3_key)
        checks to see if a s3 key path exists in a particular bucket

    get_uuid_metadata(boto_client, bucket, s3_key)
        returns metadata uuid of an s3 object if it has one, otherwise prints that one does not exist

    add_uuid_metadata(boto_client, bucket, s3_key)
        adds metadata uuid to an s3 object

    upload_s3(boto_client, local_file, bucket, s3_key, overwrite)
        uploads a file to s3 bucket

    get_csv_s3(boto_client, bucket, key)
        gets a csv file from s3 bucket using smart open library

    read_bytes_s3(boto_client, bucket, key)
        returns raw information of s3 object

    upload_archive(boto_client, vault_name, src_data)
        Add an archive to an Amazon S3 Glacier vault. The upload occurs synchronously.

    s3_to_glacier(boto_client, bucket_name, key)
        Changes storage class of s3 object from s3 -> glacier. Utilizes s3 client type

    s3_to_glacier_object_lock(boto_client, bucket_name, key, object_lock_mode, object_lock_retention)
        Changes storage class of s3 object from s3 -> glacier and places it in object lock mode. Utilizes s3 client type

    s3_restore(boto_client, bucket_name, key, days)
        Restores an object in S3 glacier back to S3 for specified amount of days

    retrieve_inventory(boto_client, vault_name)
        Initiate an Amazon Glacier inventory-retrieval job

    retrieve_inventory_results(vault_name, boto_client, job_id)
        Retrieve the results of an Amazon Glacier inventory-retrieval job
    """
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def connect(self, client_type, region):
        """
        Connects to a boto3 client

        :param client_type: str
            boto client type in which you want to access
        :param region: str
            name of aws region you want to access

        :return: boto3 client
            dependent on the client_type parameter
        """

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
        """
        Checks to see if a s3 key path exists in a particular bucket

        :param bucket: str
            name of bucket
        :param s3_key: str
            key path of s3 object in bucket

        :return: boolean
            True if exists , False otherwise
        """
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
        """
        Returns metadata uuid of an s3 object if it has one, otherwise prints that one does not exist

        :param boto_client: boto s3 resource
            utilizes boto s3 resource client type
        :param bucket: str
            name of bucket
        :param s3_key: str
            key path of object you are trying to access in bucket

        :return: str
            metadata uuid in string format
        """
        obj_uuid = None
        self.logger.debug("Get metadata")
        self.logger.info("bucket: " + bucket)
        self.logger.info("key: " + s3_key)

        s3_object = boto_client.Object(bucket, s3_key)
        s3_metadata = s3_object.metadata

        self.logger.debug("s3_metadata: " + str(s3_metadata))

        if 'object-uuid' in s3_metadata:
            obj_uuid = s3_metadata['object-uuid']
            self.logger.info("Retrieved object uuid: " + obj_uuid)
        else:
            self.logger.info("No uuid found in metadata")

        return obj_uuid

    def add_uuid_metadata(self, boto_client, bucket, s3_key):
        """
        Adds metadata uuid to an s3 object

        :param boto_client: boto s3 resource
            utilizes boto s3 resource type
        :param bucket: str
            name of bucket
        :param s3_key: str
            key path of object you are trying to access

        :return: str
            returns created uuid in string format
        """
        self.logger.info("Adding uuid to object metadata")
        obj_uuid = str(uuid.uuid4())
        s3_object = boto_client.Object(bucket, s3_key)
        s3_object.metadata.update({'object-uuid': obj_uuid})
        s3_object.copy_from(
            CopySource={'Bucket': bucket, 'Key': s3_key},
            Metadata=s3_object.metadata, MetadataDirective='REPLACE' )
        return obj_uuid

    def upload_s3(self, boto_client, local_file, bucket, s3_key, overwrite):
        """
        Uploads a file to s3 bucket

        :param boto_client: s3 client
            utilizes boto s3 client type
        :param local_file: str
            path of local file you want to upload
        :param bucket: str
            name of bucket
        :param s3_key: str
            key path that you want the object to have in the bucket
        :param overwrite: boolean
            whether or not you want to overwrite information

        :return: boolean
            True if upload successful, false otherwise
        """
        self.logger.debug("Uploading to s3")

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
                self.logger.error("File to upload was not found. Path: "+local_file)
                return False

    def get_csv_s3(self, boto_client, bucket, key):
        """
        gets a csv file from s3 bucket using smart open library

        :param boto_client: session
            utilizes boto session type
        :param bucket: str
            name of bucket
        :param key: str
            key path of object in bucket

        :return: smart open file
        """
        url = "s3://" + bucket + "/" + key
        sm_open_file = sm_open(url, 'r', transport_params={'session': boto_client})
        return sm_open_file

    def read_bytes_s3(self, boto_client, bucket, key):
        """
        Returns raw information of s3 object

        :param boto_client: s3 boto
            utilizes s3 boto client type
        :param bucket: str
            name of bucket
        :param key: str
            key path of object in s3 bucket in which you are trying to read its contents

        :return: StreamingBody()
            raw object data
        """
        # Create a file object using the bucket and object key.
        fileobj = boto_client.get_object(
            Bucket=bucket,
            Key=key
        )
        # open the file object and read it into the variable filedata.
        filedata = fileobj['Body'].read()
        return filedata

    def upload_archive(self, boto_client, vault_name, src_data):
        """
        Add an archive to an Amazon S3 Glacier vault. The upload occurs synchronously.

        :param boto_client: glacier boto
            utilizes boto glacier type
        :param vault_name: string
            name of vault that you want to upload
        :param src_data: bytes/str
            bytes of data or string reference to file spec

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
        """
        Changes storage class of s3 object from s3 -> glacier. Utilizes s3 client type

        :param boto_client: boto s3
            utlizes boto s3 client type
        :param bucket_name: str
            name of bucket
        :param key: str
            key path of object in bucket

        :return: str
            boto response after changing storage class
        """
        # reads the file data in s3 and store into variable to pass into put_object
        filedata = self.read_bytes_s3(boto_client, bucket_name, key)

        response = boto_client.put_object(Body=filedata, Bucket= bucket_name,StorageClass='GLACIER', Key=key)
        print(response)
        return response

    def s3_to_glacier_object_lock(self, boto_client, bucket_name, key, object_lock_mode, object_lock_retention):
        """
        Changes storage class of s3 object from s3 -> glacier and places it in object lock mode. Utilizes s3 client type

        :param boto_client: s3 boto client
            Utilizes s3 boto client type
        :param bucket_name: str
            name of bucket
        :param key: str
            key path of object
        :param object_lock_mode: str
            'GOVERNANCE'|'COMPLIANCE'
        :param object_lock_retention: datetime()
            how long you want the object to be locked i.e. datetime(2022, 1, 1)

        :return: str
            boto client response after object lock process
        """
        # reads the file data in s3 and store into variable to pass into put_object
        filedata = self.read_bytes_s3(boto_client,bucket_name,key)

        response = boto_client.put_object(Body=filedata, Bucket= bucket_name,StorageClass='GLACIER', Key=key, ObjectLockMode = object_lock_mode, ObjectLockRetainUntilDate=object_lock_retention)
        print(response)
        return response

    def s3_restore(self, boto_client, bucket_name, key, days):
        """
        Restores an object in S3 glacier back to S3 for specified amount of days

        :param boto_client: s3 resource
            uses s3 resource client type
        :param bucket_name: str
            name of bucket
        :param key: str
            key path of s3 object
        :param days: int
            number of days to be restored

        :return: str
            status of object after restoration process
        """

        # create bucket object
        obj = boto_client.Object(bucket_name, key)

        # Days refers to lifetime of the active copy in days
        restore_request = {'Days': days}

        # restores the object
        obj.restore_object(RestoreRequest=restore_request)

        # returns status of object retrieval
        return obj.restore


    def retrieve_inventory(self, boto_client, vault_name):
        """
        Initiate an Amazon Glacier inventory-retrieval job

        To check the status of the job, call Glacier.Client.describe_job()
        To retrieve the output of the job, call Glacier.Client.get_job_output()

        :param boto_client: glacier boto client
            utilizes boto glacier client
        :param vault_name: string
            name of vault that you want to retrieve information from

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
        """
        Retrieve the results of an Amazon Glacier inventory-retrieval job

        :param vault_name: string
            name of vault in which you want to retrieve information
        :param boto_client: glacier boto
            utilizes glacier boto client type
        :param job_id: string
            The job ID was returned by Glacier.Client.initiate_job()

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
