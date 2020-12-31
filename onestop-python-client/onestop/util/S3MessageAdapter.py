import logging
import yaml
from onestop.info.ImMessage import ImMessage
from onestop.info.FileMessage import FileMessage
from onestop.info.Link import Link
from onestop.util.ClientLogger import ClientLogger
from onestop.util.S3Utils import S3Utils
import csv


class S3MessageAdapter:

    def __init__(self, conf_loc):
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def transform(self, recs):
        self.logger.info("Transform!")
        im_message = None
        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs
        im_message = ImMessage()
        im_message.links = []

        pos = rec['s3']['object']['key'].rfind('/') + 1

        im_message.alg = "MD5"  # or perhaps Etag
        # # REVIEW  ME what to do if multipart upload
        im_message.alg_value = rec['s3']['object']['eTag']

        file_name = str(rec['s3']['object']['key'])[pos:]
        im_message.file_name = file_name
        im_message.file_size = rec['s3']['object']['size']
        im_message.file_format = self.conf['format']
        im_message.headers = self.conf['headers']

        relationship = {'type': str( self.conf['type'] ),
                        'id': str( self.conf['collection_id'] )}
        im_message.append_relationship(relationship)

        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        s3_obj_uri = "s3://" + bucket + "/" + s3_key
        print('S3 URI: ' + str(s3_obj_uri))
        file_message = FileMessage(s3_obj_uri, "ARCHIVE", True, "Amazon:AWS:S3", False)

        im_message.append_file_message(file_message)

        access_obj_uri = self.conf['access_bucket'] + "/" + rec['s3']['object']['key']
        print('Access Object uri: ' + str(access_obj_uri))

        file_message = FileMessage(access_obj_uri, "ACCESS", False, "HTTPS", False)

        # file_message.fl_lastMod['lastModified'] = TBD ISO conversion to millis

        im_message.append_file_message(file_message)

        # Looks to see if the file is a csv file
        lon, lat, time = None, None, None
        if '.csv' in str(s3_key):
            # Use S3Utils to read the file as a raw text
            s3_utils = S3Utils("config/aws-util-config-dev.yml", "config/credentials.yml")
            s3 = s3_utils.connect('s3', s3_utils.conf['s3_region'])
            file_data = s3_utils.read_bytes_s3(s3, bucket, s3_key)

            # Extract the appropriate fields
            lines = file_data.decode('utf-8').split('\n')
            for row in csv.DictReader(lines):
                # Only need to look at first line because these fields consistent throughout the file
                lon = float(row['LON'])
                lat = float(row['LAT'])
                time = row['TIME']
                break


        # Discovery block
        im_message.discovery['title'] = file_name
        im_message.discovery['parentIdentifier'] = self.conf['collection_id']
        im_message.discovery['fileIdentifier'] = "gov.noaa.ncei.csb:" + file_name[:-4]
        im_message.coordinates.append([lon,lat])
        im_message.coordinates.append([lon, lat])
        im_message.coordinates.append([lon, lat])
        im_message.coordinates.append([lon, lat])
        im_message.temporalBounding= {'beginDate': time, 'endDate': time}

        https_link = Link("download", "Amazon S3", "HTTPS", access_obj_uri)
        im_message.append_link(https_link)

        s3_link = Link("download", "Amazon S3", "Amazon:AWS:S3", s3_obj_uri)
        im_message.append_link(s3_link)

        payload = im_message.serialize()
        print(payload)


        return payload
