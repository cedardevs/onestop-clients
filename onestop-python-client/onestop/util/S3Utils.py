import logging
import yaml
import uuid
import boto3
import botocore
from botocore.exceptions import ClientError

from onestop.util.ClientLogger import ClientLogger


class S3Utils:
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, "DEBUG", False)

        self.logger.info("Initializing " + self.__class__.__name__)

    def connect(self, client_type, region):

        if client_type == "s3":
            boto_client = boto3.client("s3", aws_access_key_id=self.cred['sandbox']['access_key'],
                                       aws_secret_access_key=self.cred['sandbox']['secret_key'])
        if client_type == "glacier":
            boto_client = boto3.client("glacier", region_name=region, aws_access_key_id=self.cred['sandbox']['access_key'],
                                       aws_secret_access_key=self.cred['sandbox']['secret_key'])
        return boto_client

    def objectkey_exists(self, s3, bucket, s3_key):
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
        self.logger.debug("Get metadata")
        response = boto_client.head_object(Bucket=bucket, Key=s3_key)
        self.logger.info("bucket: " + bucket)
        self.logger.info("key: " + s3_key)
        self.logger.info("object-uuid: " + response['ResponseMetadata']['HTTPHeaders']['x-amz-meta-object-uuid'])
        return response['ResponseMetadata']['HTTPHeaders']['x-amz-meta-object-uuid']

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
                print("Upload Successful")
                return True
            except FileNotFoundError:
                print("The file was not found")
                return False

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
        return archive
