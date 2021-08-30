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
                print("conf:" + str(self.conf))
                print("conf type:" + str(type(self.conf)))
                self.queue_url = self.conf['queue_url']
                self.region = self.conf['region']
            self.wp_config_file = wp_config_file
            self.cred_file = cred_file
            self.s3_utils = S3Utils(wp_config_file, cred_file)
                      
        except Exception as ex:
            print('exception')
            self.logger.error("Exception occured while opening config file")
            self.logger.error(sys.exc_info())
        self.set_web_publisher()

    def set_web_publisher(self):
        """
        Set WebPublisher instance for class
        """
        try:
            with open(self.cred_file) as f:
                creds = yaml.load(f, Loader=yaml.FullLoader)
                registry_username = creds['registry']['username']
                registry_password = creds['registry']['password']
        except Exception as ex:
            print('exception')
            self.logger.error("Exception occured while opening credentials file")
            self.logger.error(sys.exc_info())
        try:
            with open(self.wp_config_file) as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                registry_base_url = conf['registry_base_url']
                onestop_base_url = conf['onestop_base_url']
                host_name = conf.get("host","")
        except Exception as ex:
            print('exception')
            self.logger.error("Exception occured while opening wp config file")
            self.logger.error(sys.exc_info())
        try:
            self.wp = WebPublisher(registry_base_url, registry_username, registry_password, onestop_base_url, log_level="INFO", host=host_name)
        except Exception as ex:
            self.logger.error("Exception occured while creating wp")
            self.logger.error(sys.exc_info())
            print("ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROR")

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
            region_name=self.region)
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
        print("filename:" + filename)
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
        #TODO fix metadata for target
        #TODO parent id for source 
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
        #TODO set parent id to default here, use source_dict other spot
        #dl_mes.parentDoi ="5b58de08-afef-49fb-99a1-9c5d5c003bde"
        dl_mes.parentIdentifier = "6b4f0954-628e-486e-914e-ce2dffffca90"
        west = meta_dict.get('west', None)
        east = meta_dict.get('east', None)
        south = meta_dict.get('south', None)
        north = meta_dict.get('north', None)
        begin_dt = meta_dict.get('beginDate', None)
        end_dt = meta_dict.get('endDate', None)
        dl_mes.begin_dt = begin_dt
        dl_mes.end_dt = end_dt
        dl_mes.keywords = meta_dict.get('keywords', None)
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
            MaxNumberOfMessages=1,
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
                print("body type = " + str(type(body)))
                print("body val = " + str(body))
                if 'Message' in body:
                    body_message = json.loads(body['Message'])
                    print("message type = " + str(type(body_message)))
                    print("message val = " + str(body_message))
                    if 'Records' in body_message:
                        print("type(body_message['Records']):" + str(type(body_message['Records'])))
                        msg_records = body_message['Records']
                        #print(len(msg_records))
                        print("msg_records:")
                        print(msg_records)
                        #uncomment first line, comment second line to clear SQS queue
                        #is_success = True 
                        is_success = self.process_msg_records(msg_records)
                        print("is_success:" + str(is_success))
                        indx_process = indx_process + 1
                    else:
                        print("no records in body message")
                else:
                    print('no Message in body')
                
                if is_success:
                    print("deleting message:" + messages[indx]["ReceiptHandle"])
                    response = sqs_client.delete_message(QueueUrl=self.queue_url,ReceiptHandle=messages[indx]["ReceiptHandle"])
                    print("delete message response:" + str(response))
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
            is_success = True
        else:
            print('no records at this time')
            is_success = True
        return is_success

    def process_file(self, localfile, s3Key, s3Bucket, S3Region, endpoint_url, lastModified, file_size=None, sha256=None):
        """
        Perform metadata extraction for file, type information or AWS metadata
        :param localfile: string for path to source file
        :param s3Key: AWS S3 Key for source file (contains path or original file name if tar file)
        :param s3Bucket: AWS S3 Bucket for source file
        :param s3Region: AWS S3 region for source file
        :param endpoint_url: string representing endpoint for source AWS S3 bucket
        :param lastModified: timestamp for time source s3Key file was last modified
        :param file_size: file size in byte of source S3Key file
        :param sha256: string of sha256 ash from source S3Key file metadata
        :return: DataLakeMessage populated or None
        """
        filename = localfile.split('/')[-1]
        source_dict = self.detect_source_type(s3Key)
        if source_dict is not None:
            source_type = source_dict.get("type", None)
            if source_type is not None:
                tag_dict = self.conf["tag-lookup"][source_type]
            else:
                tag_dict = {}
        else:
            tag_dict = {}
        #get initial dictionary from file by regex
        meta_dict = self.extractMetadata(filename)
        if True:

            #populate object with dictionary and enrich with known information about file
            dl_mes = self.createMetadataMessage(meta_dict)
            #transform data in object for use in JSON
            dl_mes = self.transformMetadata(dl_mes)

            
            dl_mes.file_name = filename
            dl_mes.file_size = file_size
            # "target_datalake" is hard-coded
            dl_mes.s3Bucket = self.conf["targets"]["target_datalake"]["bucket"]   
            dl_mes.s3Key = s3Key
            dl_mes.s3Dir = 's3://' + s3Bucket + '/' + s3Key.rsplit('/',1)[0] + '/'
            dl_mes.s3Path = dl_mes.s3Dir + filename
            #TODO: set parent id and parentuuid with source_dict
            s3UrlStr = '{}/{}/{}'.format(endpoint_url, dl_mes.s3Bucket, dl_mes.s3Key)
            dl_mes.s3Url =s3UrlStr
            link = Link("download", "Amazon S3", "HTTPS", s3UrlStr)
            dl_mes.append_link(link)
            chk_sums = {}
            chk_sums['checksum_algorithm'] = "SHA256"
            chk_sums['checksum_value'] = sha256
            
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
            try:
                self.copy_object_to_target(s3Bucket, s3Key, target_dict, tag_dict)
                if dl_mes.alg_value is not None:
                    is_ok = self.verify_checksum(dl_mes.s3Bucket, s3Key,  S3Region, dl_mes.alg_value)
                    if not is_ok:
                        self.logger.error(dl_mes.uri + " sha256 error")
            except Exception as e:
                self.logger.error("Exception copying: " + s3Bucket + ", " + s3Key)
                self.logger.error(e)
       
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

    def copy_object_to_target(self, s3_bucket, s3_key, target_dict, tag_dict):
        """
        Copy object to S# Target bucket and update tag
        Use same key
        :param target_dict: dictionary representing info about target
        :param s3_bucket: string for source S3 bucket
        :param s3_key: string for source s3 key
        """
        
        self.logger.info("copy_object_to_target")
        print("target_dict:" + str(target_dict))
        target_bucket = target_dict.get("bucket", None)
        is_external = target_dict.get("external", False)
        target_region = target_dict.get("region", None)
        if is_external:
            ext_access_key = target_dict.get("ext_access_key", None)
            ext_secret_key = target_dict.get("ext_secret_key", None)
            
            if ext_access_key is not None:
                ext_access_key_id = self.get_secret_value(ext_access_key, self.region)
            if ext_secret_key is not None:
                ext_secret_access_key = self.get_secret_value(ext_secret_key, self.region)
            s3_resource = boto3.resource("s3", aws_access_key_id=ext_access_key_id, \
                aws_secret_access_key=ext_secret_access_key,
                region_name=target_region)
            print("length of keys, should not be 0")
            print(len(ext_secret_access_key))
            print(len(ext_access_key_id))
            print("*******************************************")
        else:
            s3_resource = boto3.resource('s3', region_name=target_region)
        copy_source = {
            'Bucket': s3_bucket,
            'Key': s3_key
             }
        print("s3_key:" + s3_key)
        print("target_bucket:" + target_bucket)
        print("s3_bucket:" + s3_bucket)
        bucket = s3_resource.Bucket(target_bucket)
        response = bucket.copy(copy_source, s3_key)
        print("response from bucket copy: " + str(response))
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
            s3Region = record.get("s3").get("object").get("region")
            #file size in bytes
            s3Key = s3Key.replace("%3A",":")
            s3Filesize = record.get('s3').get('object').get('size')
            print("s3Bucket: " + s3Bucket)
            print("s3Key: " + s3Key)
            s3CatalogHead = s3_client.head_object(Bucket = s3Bucket, Key = s3Key)
            lastModified = int(s3CatalogHead['LastModified'].timestamp()*1000)

            print("s3CatalogHead: " + str(s3CatalogHead))
            sha256 = s3CatalogHead["Metadata"].get("sha256", None)
            if sha256 is None:
                self.logger.error("sha256 not found for " + s3Bucket + "/" + s3Key)
            filename = s3Key.split('/')[-1]
            endpoint_url = s3_client.meta.endpoint_url
            #download object
            #duplicate directory structure of bucket/key?
            #one object can have multiple files
            if 'tar' in filename and False:
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
                                s3Region, endpoint_url, lastModified)

                            if dl_mes is not None:
                                dl_mes_list.append(dl_mes)
                else:
                    dl_mes = self.process_file(filename, s3Key, s3Bucket, s3Region, endpoint_url, lastModified)
                    if dl_mes is not None:
                        dl_mes_list.append(dl_mes)

            else:
                dl_mes = self.process_file(filename, s3Key, s3Bucket, endpoint_url, lastModified, s3Filesize, sha256)
                if dl_mes is not None:
                    dl_mes_list.append(dl_mes)
            
        return dl_mes_list

    def verify_checksum(self, s3Bucket, dest_path, s3Region, sha256):
        """
        from NCCF base class, SHA1 algorithm
        :param s3Bucket: string for target S3 bucket name of file
        :param dest_path: string for target S3 key of file
        :param s3Region: string for region for target S3
        :param sha256: string for sha256 hash for file
        :return: dictionary of checksum information
        """
        #TODO: convert to SHA256?
        #TODO: retrieve value in place in bucket
        s3_client = boto3.client('s3', region_name=s3Region)
        fileobj = s3_client.get_object(
            Bucket=s3Bucket,
            Key=dest_path
            )
        # open the file object and read it into the variable filedata.
        filedata = fileobj['Body'].read()
        s3_sha = hashlib.sha256(filedata).hexdigest()
        result = s3_sha == sha256
        return result
        
      

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
            print("json_payload:" + json_payload)
            if send_to_onestop:
                print("sending to OneStop")
                s3_resource = self.s3_utils.connect("s3_resource", None)
                #object_uuid = self.s3_utils.get_uuid_metadata(s3_resource, dl_mes.s3Bucket, dl_mes.s3Key)
                object_uuid = dl_mes.fileIdentifier
                registry_response = self.wp.publish_registry("granule", object_uuid, json_payload, "POST")
                if registry_response.status_code == 200:
                    print("REGISTRY RESPONSE")
                    print(registry_response.json())
                    print("registry dict" + str(registry_response.__dict__))
                    #is_success logic
                    is_success = True
                else:
                    is_success = False
                    print("Onestop response error")
                    print("registry dict" + str(registry_response.__dict__))
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
        target_region = target_dict.get("region")
        if is_external:
        
            ext_access_key = target_dict.get("ext_access_key", None)
            ext_secret_key = target_dict.get("ext_secret_key", None)
            if ext_access_key is not None:
                ext_access_key_id = self.get_secret_value(ext_access_key, self.region)
            if ext_secret_key is not None:
                ext_secret_access_key = self.get_secret_value(ext_secret_key, self.region)
            s3_client = boto3.client('s3',  region_name=target_region,\
                aws_access_key_id=ext_access_key_id, \
                aws_secret_access_key=ext_secret_access_key)
        else:
            s3_client = boto3.client('s3',  region_name=target_region)
        
        
        tag_list = [{'Key': str(k), 'Value': str(v)} for k, v in tag_dict.items()]
        print("tag_list:" + str(tag_list))
        response = s3_client.put_object_tagging(
            Bucket=target_bucket,
            Key=s3_key,
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
        print("messages: " + str(messages))
        indx_proc = self.get_records_from_messages(sqs_client, messages)
        
        print("indx_proc:" + str(indx_proc))

    def run_search_process(self):
        """
        Call search URL on OneStop
        """
        print("get_granules_onestop")
        par_id = "6b4f0954-628e-486e-914e-ce2dffffca90"
        response = self.wp.get_granules_onestop(par_id)
        print("SEARCH get_granules RESPONSE")
        print(response.text)
        print("******************************")
        print("search registry, collection")
        response = self.wp.search_registry("collection", par_id)
        print("SEARCH registry RESPONSE")
        print(response.status_code)
        print("***************************")
        payload = '{"queries":[],"filters":[{"type":"collection","values":["' + par_id +  '"]}],"facets":true,"page":{"max":50,"offset":0}}'
        self.logger.info("Getting granules for id=" + par_id)

        response = self.wp.search_onestop("collection", payload)
        self.logger.info("Response: "+str(response))
        print("SEARCH collection registry RESPONSE")
        print(response.text)



    def run_interval_tracker(self):
        """
        Wake up logic, entry point for class
        """
        s = sched.scheduler(tm.time, tm.sleep)
        self.logger.info('starting GEFS extraction')
        self.run_process()
        #self.run_search_process()
        while False:
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
    #config_path = "C:\\Users\\jeanne.lane\\Documents\\Projects\\onestop-clients\\onestop-python-client\\config\\"
    dl_ext_config = config_path + "datalake-extract-config.yml"
    wp_config = config_path + "web-publisher-config-dev.yml"
    cred_config = config_path + "credentials-template.yml"
    dl_ext = DataLakeExtractor(dl_ext_config, wp_config, cred_config)

    dl_ext.run_interval_tracker()

if __name__ == '__main__':
    run()

