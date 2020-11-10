import logging
from datetime import datetime, timezone
import yaml
import uuid
import json
import boto3
import botocore


class S3Utils:
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.setup_logger(self.__class__.__name__, False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def setup_logger(self, log_name, create_file=False):

        # create logger
        self.logger = logging.getLogger(self.__class__.__name__)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.conf['log_level'] == "DEBUG":
            self.logger.setLevel(level=logging.DEBUG)
        else:
            if self.conf['log_level'] == "INFO":
                self.logger.setLevel(level=logging.INFO)
            else:
                self.logger.setLevel(level=logging.ERROR)

        fh = None
        if create_file:
            # create file handler for logger.
            fh = logging.FileHandler(log_name)
            fh.setFormatter(formatter)

        # create console handler for logger.
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # add handlers to logger.
        if create_file:
            self.logger.addHandler(fh)

        self.logger.addHandler(ch)

    def connect(self):
        boto_client = boto3.client("s3", aws_access_key_id=self.cred['sandbox']['access_key'],
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

    def upload_file(self, boto_client, local_file, bucket, s3_key, overwrite):
        self.logger.debug("Receive messages")

        key_exists = False
        obj_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'data.noaa.gov'))

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