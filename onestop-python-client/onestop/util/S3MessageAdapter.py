import logging
import yaml
from onestop.info.ImMessage import ImMessage
from onestop.info.FileMessage import FileMessage
from onestop.info.Link import Link
from onestop.util.ClientLogger import ClientLogger
from onestop.util.S3Utils import S3Utils
from onestop.extract.CsbExtractor import CsbExtractor



class S3MessageAdapter:

    def __init__(self, conf_loc, s3_utils):
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)
        self.s3_utils = s3_utils
        self.CsbExtractor = CsbExtractor(conf_loc,s3_utils)



    def transform(self, recs):
        self.logger.info("Transform!")
        im_message = None
        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs
        im_message = ImMessage()
        im_message.links = []

        s3_bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        pos = s3_key.rfind('/') + 1

        im_message.alg = "MD5"  # or perhaps Etag
        # # REVIEW  ME what to do if multipart upload
        im_message.alg_value = rec['s3']['object']['eTag']

        file_name = str(s3_key)[pos:]
        im_message.file_name = file_name
        im_message.file_size = rec['s3']['object']['size']
        im_message.file_format = self.conf['format']
        im_message.headers = self.conf['headers']

        relationship = {'type': str( self.conf['type'] ),
                        'id': str( self.conf['collection_id'] )}
        im_message.append_relationship(relationship)

        s3_obj_uri = "s3://" + s3_bucket + "/" + s3_key
        print('S3 URI: ' + str(s3_obj_uri))
        file_message = FileMessage(s3_obj_uri, "ARCHIVE", True, "Amazon:AWS:S3", False)

        im_message.append_file_message(file_message)

        access_obj_uri = self.conf['access_bucket'] + "/" + s3_key
        print('Access Object uri: ' + str(access_obj_uri))

        file_message = FileMessage(access_obj_uri, "ACCESS", False, "HTTPS", False)

        # file_message.fl_lastMod['lastModified'] = TBD ISO conversion to millis

        im_message.append_file_message(file_message)

        # Looks to see if the file is a csv file
        if self.CsbExtractor.is_csv(s3_key):
            # first line of the csv file
            lines = self.CsbExtractor.get_line(s3_bucket,s3_key)

            # Min max of lon and latitude
            max_lon = self.CsbExtractor.get_max_numeric(lines, 'LON')
            max_lat = self.CsbExtractor.get_max_numeric(lines, 'LAT')
            min_lon = self.CsbExtractor.get_min_numeric(lines, 'LON')
            min_lat = self.CsbExtractor.get_min_numeric(lines, 'LAT')

            end_date_str = self.CsbExtractor.get_max_datetime(lines, 'TIME')
            begin_date_str = self.CsbExtractor.get_min_datetime(lines,'TIME')

            coords = self.CsbExtractor.extract_coords(lines, max_lon, max_lat, min_lon, min_lat)


        # Discovery block
        im_message.discovery['title'] = file_name
        im_message.discovery['parentIdentifier'] = self.conf['collection_id']
        im_message.discovery['fileIdentifier'] = self.conf['file_identifier_prefix'] + file_name[:-4]
        for coord in coords:
            im_message.coordinates.append(coord)
        im_message.temporalBounding= {'beginDate': begin_date_str, 'endDate': end_date_str }

        https_link = Link("download", "Amazon S3", "HTTPS", access_obj_uri)
        im_message.append_link(https_link)

        s3_link = Link("download", "Amazon S3", "Amazon:AWS:S3", s3_obj_uri)
        im_message.append_link(s3_link)

        payload = im_message.serialize()
        print(payload)


        return payload
