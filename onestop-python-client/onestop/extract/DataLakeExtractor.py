import boto3
import json
import re
import datetime
import logging
import hashlib
import os
import uuid
import time as tm
import sched
from sys import getsizeof
from datetime import timedelta
import  tarfile
import shutil
import sys
import yaml
import numpy as np

from onestop.util.S3Utils import S3Utils
from onestop.WebPublisher import WebPublisher
from onestop.info.DataLakeMessage import DataLakeMessage
from onestop.info.Link import Link

gefs_regex = r"(?P<variable>[a-z_]*)_(?P<run_dt>\d{10})_(?P<member>[cp]\d{2})\.grib2$"
gefs_file = "ugrd_pres_2020121102_c02.grib2"

"""
Class for extracting metadata out of Data Lake data

Similar interface to base class for NCCF

Author: Jeanne Lane, SAIC
"""

class DataLakeExtractor():
    def __init__(self, conf_loc, wp_config_file, cred_file):
        """
        Class constructor
        """
        self.logger = logging.getLogger("Rotating Log")
        self.logger.setLevel(logging.DEBUG)
        try:
            with open(conf_loc) as f:
                self.conf = yaml.load(f, Loader=yaml.FullLoader)
                print(self.conf)
                print(type(self.conf))
                self.queue_url = self.conf['queue_url']
                self.region = self.conf['region']
            self.wp_config_file = wp_config_file
            self.cred_file = cred_file
            self.s3_utils = S3Utils(wp_config_file, cred_file)
        except Exception as ex:
            print('exception')
            self.logger.error("Exception occured while opening config file")
            self.logger.error(sys.exc_info())
       

    def get_secret_value(self, secret_key, region):
        """
        Obtains secret from AWS Secret Manager
        :param secret_key: input key for secret
        :param region: AWS region 
        :return: string Secret Value
        """
        #eventually move to util class
        secret_value = ""
        sm_client = boto3.client(service_name='secretsmanager',
            region_name=region)
        get_secret_value_response = sm_client.get_secret_value(
            SecretId=secret_key)
        secret_value = get_secret_value_response['SecretString']
        return secret_value

    def extractMetadata(self, filename):
        """
        Extract metadata from file and return in dictionary
        :param filename: string for file name to be extracted
        :return: dictionary of metadata extracted from file
        """
        meta_dict = {}
        gefs = re.match(gefs_regex, filename)
        print("testing regex")
        print(filename)
        if gefs:

            meta_dict = self.parse_gefs_filename(gefs)
            meta_dict['headers'] = "" # can add method to extract gefs headers?
            meta_dict['optAttrFileInfo'] = "" #can add method to extract additional information
            #east,west,south,north
            meta_dict['type'] = 'gefs'

        else:
            meta_dict['type'] = 'n/a'
            print("no matching pattern")
        return meta_dict

    def createMetadataMessage(self, meta_dict):
        """
        Creates metadata object with information that stays the same for dataset
        :param meta_dict: dictionary containing metadata that has been extracted from file
        :return: enriched DataLakeMessage object
        """
        #TODO parent id for source :Erin
        dl_mes = DataLakeMessage()
        #file information
        dl_mes.file_format = "grib2"
        
        #relationships
        dl_mes.parentUuid = "6b4f0954-628e-486e-914e-ce2dffffca90"
        dl_mes.rel_type = "COLLECTION"
        #discovery
        dl_mes.type = "ACCESS"
        dl_mes.restricted = False
        dl_mes.service_type = "Amazon:AWS:S3"
        dl_mes.asynchronous = False
        dl_mes.deleted = False
        #dl_mes.parentDoi ="5b58de08-afef-49fb-99a1-9c5d5c003bde"
        dl_mes.parentIdentifier = "6b4f0954-628e-486e-914e-ce2dffffca90"
        west = meta_dict.get('west', None)
        east = meta_dict.get('east', None)
        south = meta_dict.get('south', None)
        north = meta_dict.get('north', None)
        begin_dt = meta_dict['beginDate']
        end_dt = meta_dict['endDate']
        dl_mes.begin_dt = begin_dt
        dl_mes.end_dt = end_dt
        dl_mes.keywords = meta_dict['keywords']
        if west is not None:
            polyStr = (
                " [  \n [ \n [ " +
                str(west) + ", " + str(north) + "], \n [" +
                str(west) + ", " + str(south) + "], \n [" +
                str(east) + ", " + str(south) + "], \n [" +
                str(east) + ", " + str(north) + "], \n [" +
                str(west) + ", " + str(north) +
                "] \n ] \n ] \n" )
            dl_mes.coordinates = polyStr
        return dl_mes


    def transformMetadata(self, gefs_mes):
        """
        Perform formatting changes on existing metadata in dictionary
        :param gefs_mes: DataLakeMessage object
        :return: DataLakeMessage that is ready to be sent by WebPublisher
        """
        if gefs_mes.begin_dt is not None:
            beginTimeStr = gefs_mes.begin_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            gefs_mes.begin_date_str = beginTimeStr
        if gefs_mes.end_dt is not None:
            endTimeStr = gefs_mes.end_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            gefs_mes.end_date_str = endTimeStr
        return gefs_mes


    def parse_gefs_filename(self, gefs_regex_match):
        """
        Extract metadata from filename
        :param gefs_regex_match: regex match group list
        :return: dictionary of parsed data
        """
        variable = ""
        run_dt = ""
        member = ""
        try:
            variable = gefs_regex_match.group('variable')
            run_dt = gefs_regex_match.group('run_dt')
            member = gefs_regex_match.group('member')
        except IndexError:
            print("gefs file name formed incorrectly")
        gefs_dict = {"variable": variable, "begin_dt": run_dt, "member": member}
        return gefs_dict

    # Create SQS client
    def receive_messages(self, sqs_client):
        """
        Request and receive messages from AWS SQS, retrieve messages from response object, return list
        :param sqs_client: client to AWS SQS service
        :return: list of dictionaries representing messages
        """
        messages = []
        

        # Receive message from SQS queue
        response = sqs_client.receive_message(
            QueueUrl=self.queue_url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ]
        )

        if 'Messages' in response:
            messages = response['Messages']
        else:
            print("no messages in response")
        return messages

    def get_records_from_messages(self, sqs_client, messages):
        """
        Retrieve records from extracted AWS SQS messages
        Delete message once record successfully processed
        :param sqs_client: client to AWS SQS service
        :param messages: messages that were extracted from AWS SQS
        :return: int for number of processed messages
        """
        records = []
        indx_process = 0
        for indx in range(len(messages)):
            print("indx = " + str(indx))
            if 'Body' in messages[indx]:
                body = json.loads(messages[indx]['Body'])
                #print(type(body))
                #print(body)
                if 'Message' in body:
                    body_message = json.loads(body['Message'])
                    #print(type(body_message))
                    #print(body_message)
                    if 'Records' in body_message:
                        #print(type(body_message['Records']))
                        msg_records = body_message['Records']
                        #print(len(msg_records))
                        #print(msg_records)
                        #uncomment first line, comment second line to clear SQS queue
                        #is_success = True 
                        is_success = self.process_msg_records(msg_records)
                        indx_process = indx_process + 1
                    else:
                        print("no records in body message")
                else:
                    print('no Message in body')
                
                if is_success:
                    print("deleting message:" + messages[indx]["ReceiptHandle"])
                    sqs_client.delete_message(QueueUrl=self.queue_url,ReceiptHandle=messages[indx]["ReceiptHandle"])
            else:
                print('no body in outer message')
        return indx_process

    def process_msg_records(self, records):
        """
        :param records: list of dictionaries for records from S3 events > SNS > SQS chain
        """
        is_success = False
        if len(records) > 0:
            dl_mes_list = self.process_records(records)
            self.publishToOneStop(dl_mes_list)
            
        else:
            print('no records at this time')
            is_success = True
        return is_success

    def process_file(self, localfile, s3Key, s3Bucket, endpoint_url, lastModified, file_size=None):
        """
        Perform metadata extraction for file, type information or AWS metadata
        :param localfile: string for path to source file
        :param s3Key: AWS S3 Key for source file (contains path or original file name if tar file)
        :param s3Bucket: AWS S3 Bucket for source file
        :param endpoint_url: string representing endpoint for source AWS S3 bucket
        :param lastModified: timestamp for time source s3Key file was last modified
        :param file_size: file size in byte of source S3Key file
        :return: DataLakeMessage populated or None
        """
        filename = localfile.split('/')[-1]
        source_dict = self.detect_source_type(s3Key)
        source_type = source_dict["type"]
        tag_dict = self.conf["tag-lookup"]
        #get initial dictionary from file by regex
        meta_dict = self.extractMetadata(filename)
        if True:

            #populate object with dictionary and enrich with known information about file
            dl_mes = self.createMetadataMessage(meta_dict)
            #transform data in object for use in JSON
            dl_mes = self.transformMetadata(dl_mes)

            
            dl_mes.file_name = filename
            dl_mes.file_size = file_size
            dl_mes.s3Bucket = s3Bucket
            dl_mes.s3Key = s3Key
            dl_mes.s3Dir = 's3://' + s3Bucket + '/' + s3Key.rsplit('/',1)[0] + '/'
            dl_mes.s3Path = dl_mes.s3Dir + filename

            s3UrlStr = '{}/{}/{}'.format(endpoint_url, dl_mes.s3Bucket, dl_mes.s3Key)
            dl_mes.s3Url =s3UrlStr
            link = Link("download", "Amazon S3", "HTTPS", s3UrlStr)
            dl_mes.append_link(link)
            chk_sums = self.get_checksum(localfile)
            dl_mes.alg = chk_sums['checksum_algorithm']
            dl_mes.alg_value = chk_sums['checksum_value']
            dl_mes.lastModifiedMillis = lastModified
            dl_mes.optAttrFileLoc =""
            dl_mes.fileIdentifier = str( uuid.uuid4() )
        else:
            self.logger.error("error occured while parsing")
            dl_mes = None
        #publish object to target bucket
        dl_target_dict = self.conf["targets"]
        for key in dl_target_dict:
            target_dict = dl_target_dict[key]
            self.copy_object_to_target(s3Bucket, s3Key, target_dict, tag_dict)
        #TODO: put SHA256 in metadata in source and target bucket(s)
        #update dl_mes
        return dl_mes

    def detect_source_type(self, s3key):
        """
        Detect source type by S3 Key and return dictionary of source type info
        :param s3key: Key for source object
        :return: dictionary of source type info
        """
        source_dict = None
        if "source_lookup"  in self.conf:
            for key in self.conf["source_lookup"]:
                if key in s3key:
                    source_dict = self.conf["source_lookup"][key]
        else:
            self.logger.error("source_lookup missing in config")
        return source_dict

    def copy_object_to_target(self, target_dict, s3_bucket, s3_key):
        """
        Copy object to S# Target bucket and update tag
        Use same key
        :param target_dict: dictionary representing info about target
        :param s3_bucket: string for source S3 bucket
        :param s3_key: string for source s3 key
        """
        
        self.logger.info("copy_object_to_target")
        target_bucket = target_dict.get("bucket", None)
        is_external = target_dict.get("external", False)
        if is_external:
        
            ext_access_key = target_dict.get("ext_access_key", None)
            ext_secret_key = target_dict.get("ext_secret_key", None)
            if ext_access_key is not None:
                ext_access_key_id = self.get_secret_value(ext_access_key, region)
            if ext_secret_key is not None:
                ext_secret_access_key = self.get_secret_value(ext_secret_key, region)
            s3_resource = boto3.resource("s3", aws_access_key_id=ext_access_key_id, \
                aws_secret_access_key=ext_secret_access_key)
        else:
            s3_resource = boto3.resource('s3')
        copy_source = {
            'Bucket': s3_bucket,
            'Key': s3_key
             }
        bucket = s3_resource.Bucket(target_bucket)
        bucket.copy(copy_source, s3_key)
        #TODO: copy metadata
        #TODO: check sha256
        self.updateObjectTagsWithMetadata(target_dict, s3_key, tag_dict)

    def process_records(self, records):
        """
        Extract file information from record and copy file from source to targets, update meta_dict with information from record
        :param records: list of dictionaries representing records
        :return: list of DataLakeMessage objects
        """
        print('processing records')
        print(len(records))
        print("*********************************************************")
        #print(records)
        s3_client = boto3.client('s3', region_name='us-east-1')
        dl_mes_list = []
        for record in records:
            s3Bucket = record.get("s3").get("bucket").get("name")
            s3Key = record.get("s3").get("object").get("key")
            #file size in bytes
            s3Filesize = record.get('s3').get('object').get('size')
            s3CatalogHead = s3_client.head_object(Bucket = s3Bucket, Key = s3Key)
            lastModified = int(s3CatalogHead['LastModified'].timestamp()*1000)
            print(s3Key)
            print(s3Bucket)
            print(s3Filesize)
            filename = s3Key.split('/')[-1]
            endpoint_url = s3_client.meta.endpoint_url
            #download object
            #duplicate directory structure of bucket/key?
            #one object can have multiple files
            if 'tar' in localFile:
                size_limit = 5 * 10^5 #leaving this here in case I want to use more RAM
                if s3Filesize is not None and s3Filesize < size_limit:
                    objectbytes = s3_object['Body'].read()
                    fileobj = io.BytesIO(objectbytes)
                    tarf = tarfile.open(fileobj=fileobj)
                    members = tarf.getnames()
                    if len(names) > 0:
                        pass
                    print("untarred members")
                    print(members)
                    print(len(members))
                    if len(members) > 0:
                        for filename in members:
                            #need to rewrite this to make members a recursively untarred files
                            #memberFile = os.path.join(self.conf['temp_dir'], member.name)
                            #print(memberFile)
                            dl_mes = self.process_file(filename, s3Key, s3Bucket, \
                                endpoint_url, lastModified)

                            if dl_mes is not None:
                                dl_mes_list.append(dl_mes)
                else:
                    dl_mes = self.process_file(localfile, s3Key, s3Bucket, endpoint_url, lastModified)
                    if dl_mes is not None:
                        dl_mes_list.append(dl_mes)

            else:
                dl_mes = self.process_file(localFile, s3Key, s3Bucket, endpoint_url, lastModified, s3Filesize)
                if dl_mes is not None:
                    dl_mes_list.append(dl_mes)
            
        return dl_mes_list

    def get_checksum(self, localFile):
        """
        from NCCF base class, SHA1 algorithm
        :param localFile: string for path to local file
        :return: dictionary of checksum information
        """
        #TODO: convert to SHA256?
        #TODO: retrieve value in place in bucket
        checksum_dict = {}
        self.logger.info("Doing checksum")
        sha1 = hashlib.sha1()
        BUF_SIZE = 262144  # for hashing, 256KB chunks!

        with open(localFile, 'rb') as f:
            tempData = f.read(BUF_SIZE)
            while len(tempData) > 0:
                sha1.update(tempData)
                tempData = f.read(BUF_SIZE)
        sha1Val = sha1.hexdigest()
        checksum_dict['checksum_algorithm'] = "SHA1"
        checksum_dict['checksum_value'] = sha1Val
        return checksum_dict

    def publishToOneStop(self, dl_message_list):
        """
        Send serialized DataLakeMessage object list to OneStop as in format of Granular Template
        via WebPublisher
        :param dl_message_list: list of DataLakeMessage objects
        :return: boolean, True if success
        """
        send_to_onestop = True
        is_success = False
        for dl_mes in dl_message_list:
            payload = dl_mes.serialize()

            json_payload = json.dumps(payload, indent=2)
            print(json_payload)
            if send_to_onestop:
                print("sending to OneStop")
                wp = WebPublisher(self.wp_config_file, self.cred_file)
                s3_resource = self.s3_utils.connect("s3_resource", None)
                #object_uuid = self.s3_utils.get_uuid_metadata(s3_resource, dl_mes.s3Bucket, dl_mes.s3Key)
                object_uuid = dl_mes.fileIdentifier
                registry_response = wp.publish_registry("granule", object_uuid, json_payload, "POST")
                print(registry_response.json())
                #is_success logic
                is_success = True
            else:
                print("not sending to OneStop")
                is_success = True
        return is_success

    def updateObjectTagsWithMetadata(self, target_dict, s3_key, tag_dict):
        """
        Update objects with NOAA AWS Tags
        :param target_dict: dictionary of information about one target bucket
        :param s3_key: key for source and target S3 File
        :param tag_dict: dictionary of AWS Object Tag values for source type
        :return: boolean if successful response
        """
        is_success = True
        is_external = target_dict.get("external", False)
        target_bucket = target_dict.get("bucket")
        if is_external:
        
            ext_access_key = target_dict.get("ext_access_key", None)
            ext_secret_key = target_dict.get("ext_secret_key", None)
            if ext_access_key is not None:
                ext_access_key_id = self.get_secret_value(ext_access_key, region)
            if ext_secret_key is not None:
                ext_secret_access_key = self.get_secret_value(ext_secret_key, region)
            s3_client = boto3.client('s3',  region_name=self.region,\
                aws_access_key_id=ext_access_key_id, \
                aws_secret_access_key=ext_secret_access_key)
        else:
            s3_client = boto3.client('s3',  region_name=self.region)
        
        
        tag_list = [{'Key': str(k), 'Value': str(v)} for k, v in tag_dict.items()]
        response = s3_client.put_object_tagging(
            Bucket=target_bucket,
            Key=s3Key,
            Tagging={
                'TagSet': tag_list
                }
            )

        is_success = is_success and response['ResponseMetadata']['HTTPStatusCode'] == 200
        return is_success

    def run_process(self):
        """
        Run main logic: retrieve messages from S3/SNS/SQS, extract file information from messages, download file,
        extract metadata, reformat metadata to required template, and send to OneStop SNS
        """
        sqs_client = boto3.client('sqs',  region_name=self.region)
        messages = self.receive_messages(sqs_client)
        #print(messages)
        indx_proc = self.get_records_from_messages(sqs_client, messages)
        
        print(indx_proc)

    def run_interval_tracker(self):
        """
        Wake up logic, entry point for class
        """
        s = sched.scheduler(tm.time, tm.sleep)
        self.logger.info('starting GEFS extraction')
        while True:
            wake_up_interval = self.conf['sleep']  #seconds
            s.enter(wake_up_interval, 1, self.run_process, ())
            # I didn't see enter used in a loop like this in documentation
            # so I was checking to see scheduler object size changes
            self.logger.debug(str( getsizeof(s)) + str(s))
            if s is None:
                self.logger.critical( 's is None')
            s.run()



def run():
    """
    Entry point for module
    """
    print(boto3.resource.__code__.co_code)
    print(boto3.resource.__code__.co_consts)
    config_path = "/home/siteadm/onestop-clients/onestop-python-client/config/"
    config_path = "C:\\Users\\jeanne.lane\\Documents\\Projects\\onestop-clients\\onestop-python-client\\config\\"
    dl_ext_config = config_path + "datalake-extract-config.yml"
    wp_config = config_path + "web-publisher-config-dev.yml"
    cred_config = config_path + "credentials-template.yml"
    dl_ext = DataLakeExtractor(dl_ext_config, wp_config, cred_config)

    dl_ext.run_interval_tracker()

if __name__ == '__main__':
    run()

