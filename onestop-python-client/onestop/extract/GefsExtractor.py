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

from onestop.util.S3Utils import S3Utils
from onestop.WebPublisher import WebPublisher
from onestop.info.GefsMessage import GefsMessage
from onestop.info.Link import Link

gefs_regex = r"(?P<variable>[a-z_]*)_(?P<run_dt>\d{10})_(?P<member>[cp]\d{2})\.grib2$"
gefs_file = "ugrd_pres_2020121102_c02.grib2"

"""
Class for extracting metadata out of GEFS data

Similar interface to base class for NCCF

Author: Jeanne Lane, SAIC
"""

class GefsExtractor():
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
        :return: enriched GefsMessage object
        """
        gefs_mes = GefsMessage()
        #file information
        gefs_mes.file_format = "grib2"
        
        #relationships
        gefs_mes.parentUuid = "6b4f0954-628e-486e-914e-ce2dffffca90"
        gefs_mes.rel_type = "COLLECTION"
        #discovery
        gefs_mes.type = "ACCESS"
        gefs_mes.restricted = False
        gefs_mes.service_type = "Amazon:AWS:S3"
        gefs_mes.asynchronous = False
        gefs_mes.deleted = False
        #gefs_mes.parentDoi ="5b58de08-afef-49fb-99a1-9c5d5c003bde"
        gefs_mes.parentIdentifier = "6b4f0954-628e-486e-914e-ce2dffffca90"
        west = 0
        east = 359.75
        south = -90
        north = 90
        begin_dt = datetime.datetime.strptime(meta_dict['begin_dt'], '%Y%m%d%H')
        end_dt = begin_dt + timedelta(days=16)
        gefs_mes.begin_dt = begin_dt
        gefs_mes.end_dt = end_dt
        
        polyStr = (
            " [  \n [ \n [ " +
            str(west) + ", " + str(north) + "], \n [" +
            str(west) + ", " + str(south) + "], \n [" +
            str(east) + ", " + str(south) + "], \n [" +
            str(east) + ", " + str(north) + "], \n [" +
            str(west) + ", " + str(north) +
            "] \n ] \n ] \n" )
        gefs_mes.coordinates = polyStr
        return gefs_mes


    def transformMetadata(self, gefs_mes):
        """
        Perform formatting changes on existing metadata in dictionary
        :param gefs_mes: GEFSMessage object
        :return: GefsMessage that is ready to be sent by SNS
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
        :param sqs_client: client to AWS SQS service
        :param messages: messages that were extracted from AWS SQS
        :return: list of dictionaries representing extracted records
        """
        records = []
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
                        is_success = self.process_msg_records(msg_records)
                    else:
                        print("no records in body message")
                else:
                    print('no Message in body')
                print("deleting message:" + messages[indx]["ReceiptHandle"])
                if is_success:
                    sqs_client.delete_message(QueueUrl=self.queue_url,ReceiptHandle=messages[indx]["ReceiptHandle"])
            else:
                print('no body in outer message')
        return records

    def process_msg_records(self, records):
        is_success = False
        if len(records) > 0:
            gefs_msg_list = self.process_records(records)
            self.publishToOneStop(gefs_msg_list)
            gefs_tag_dict={
                "noaa:programoffice": "esrl",
                "noaa:environment": "dev",
                "noaa:lineoffice": "oar",
                "noaa:fismaid": "noaa3000",
                "noaa:taskorder": "gefs-reforecast",
                "noaa:projectid": "nccf",
                "nesdis:poc": "jeffrey.s.whitaker@noaa.gov",
                "format":"grib2"
                }

            is_success = self.updateObjectTagsWithMetadata(gefs_msg_list, gefs_tag_dict)
        else:
            print('no records at this time')
            is_success = True
        return is_success

    def process_file(self, localfile, s3Key, s3Bucket, endpoint_url, lastModified, file_size=None):
        """
        Perform metadata extraction from file, type information or AWS metadata
        :param localfile: string for path to file
        :param s3Key: AWS S3 Key for file (contains path or original file name if tar file)
        :param s3Bucket: AWS S3 Bucket for file
        :param endpoint_url: string representing endpoint for AWS S3 bucket
        :param lastModified: timestamp for time s3Key file was last modified
        :param file_size: file size in byte of S3Key file
        :return: GefsMessage populated or None
        """
        filename = localfile.split('/')[-1]
        
        #get initial dictionary from file
        meta_dict = self.extractMetadata(filename)
        if meta_dict["type"] == "gefs":

            #populate object with dictionary and enrich with known information about file
            gefs_mes = self.createMetadataMessage(meta_dict)
            #transfrom data in object for use in JSON
            gefs_mes = self.transformMetadata(gefs_mes)
            if file_size is None:
                file_size = os.path.getsize(localfile)
            gefs_mes.file_name = filename
            gefs_mes.file_size = file_size
            gefs_mes.s3Bucket = s3Bucket
            gefs_mes.s3Key = s3Key
            gefs_mes.s3Dir = 's3://' + s3Bucket + '/' + s3Key.rsplit('/',1)[0] + '/'
            gefs_mes.s3Path = gefs_mes.s3Dir + filename

            s3UrlStr = '{}/{}/{}'.format(endpoint_url, gefs_mes.s3Bucket, gefs_mes.s3Key)
            gefs_mes.s3Url =s3UrlStr
            link = Link("download", "Amazon S3", "HTTPS", s3UrlStr)
            gefs_mes.append_link(link)
            chk_sums = self.get_checksum(localfile)
            gefs_mes.alg = chk_sums['checksum_algorithm']
            gefs_mes.alg_value = chk_sums['checksum_value']
            gefs_mes.lastModifiedMillis = lastModified
            gefs_mes.optAttrFileLoc =""
            gefs_mes.fileIdentifier = str( uuid.uuid4() )
        else:
            self.logger.error("error occured while parsing")
            gefs_mes = None
        return gefs_mes


    def process_records(self, records):
        """
        Extract file information from record and download file, update meta_dict with information from record
        :param records: list of dictionaries representing records
        :return: list of GefsMessage objects
        """
        print('processing records')
        print(len(records))
        print("*********************************************************")
        #print(records)
        s3_client = boto3.client('s3', region_name='us-east-1')
        gefs_mes_list = []
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
            localFile = os.path.join(self.conf['temp_dir'], filename)
            try:
                s3_client.download_file(s3Bucket, s3Key, localFile)
                self.logger.info("Downloaded file to: " + self.conf['temp_dir'])
            except Exception as e:
                raise Exception("Unable to download file from S3: " + filename)
            #one object can have multiple files
            if 'tar' in localFile:
                try:
                    tar = tarfile.open(localFile)
                    members = tar.getmembers()
                    shutil.unpack_archive(localFile, self.conf['temp_dir'])
                    print("untarred members")
                    print(members)
                    print(len(members))
                    if len(members) > 0:
                        for member in members:
                            #need to rewrite this to make members a recursively untarred files
                            extracted = tar.extractfile(member)
                            print(member.name)
                            print(extracted.name)
                            memberFile = os.path.join(self.conf['temp_dir'], member.name)
                            print(memberFile)
                            gefs_mes = self.process_file(memberFile, s3Key, s3Bucket, endpoint_url, lastModified)
                            if gefs_mes is not None:
                                gefs_mes_list.append(gefs_mes)
                except ValueError:
                    self.logger.error("Error unpacking archive")
                    self.logger.error

            else:
                gefs_mes = self.process_file(localFile, s3Key, s3Bucket, endpoint_url, lastModified, s3Filesize)
                if gefs_mes is not None:
                    gefs_mes_list.append(gefs_mes)
        return gefs_mes_list

    def untar_members(self, members):
        """
        return a list of untarred
        """
        #TODO
        return members

    def get_checksum(self, localFile):
        """
        from NCCF base class, SHA1 algorithm
        :param localFile: string for path to local file
        :return: dictionary of checksum information
        """
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

    def publishToOneStop(self, gefs_message_list):
        """
        Send serialized GefsMessage object list to OneStop as in format of Granular Template
        via WebPublisher
        :param gefs_message_list: list of GefsMessage objects
        :return: boolean, True if success
        """
        send_to_onestop = True
        is_success = False
        for gefs_mes in gefs_message_list:
            payload = gefs_mes.serialize()

            json_payload = json.dumps(payload, indent=2)
            print(json_payload)
            if send_to_onestop:
                print("sending to OneStop")
                wp = WebPublisher(self.wp_config_file, self.cred_file)
                s3_resource = self.s3_utils.connect("s3_resource", None)
                #object_uuid = self.s3_utils.get_uuid_metadata(s3_resource, gefs_mes.s3Bucket, gefs_mes.s3Key)
                object_uuid = gefs_mes.fileIdentifier
                registry_response = wp.publish_registry("granule", object_uuid, json_payload, "POST")
                print(registry_response.json())
                #is_success logic
                is_success = True
            else:
                print("not sending to OneStop")
                is_success = True
        return is_success

    def updateObjectTagsWithMetadata(self, meta_list, tag_dict):
        """
        Update objects with NOAA AWS Tags
        :param meta_list: list of GefsMessage objects
        :return: boolean if successful response
        """

        is_success = True
        s3_client = boto3.client('s3',  region_name=self.region)
        for gefs_mes in meta_list:
            if gefs_mes != 'n/a':
                tag_list = [{'Key': str(k), 'Value': str(v)} for k, v in tag_dict.items()]
                response = s3_client.put_object_tagging(
                    Bucket=gefs_mes.s3Bucket,
                    Key=gefs_mes.s3Key,
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
        records = self.get_records_from_messages(sqs_client, messages)
        
        #print(messages)

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
    config_path = "/home/siteadm/onestop-clients/onestop-python-client/config/"
    gefs_config = config_path + "gefs-extraction-config.yml"
    wp_config = config_path + "web-publisher-config-dev.yml"
    cred_config = config_path + "credentials-template.yml"
    gefs = GefsExtractor(gefs_config, wp_config, cred_config)
    gefs.run_interval_tracker()

if __name__ == '__main__':
    run()

