import logging
import yaml
from onestop.info.ImMessage import ImMessage
from onestop.info.FileMessage import FileMessage
from onestop.info.Link import Link

class S3MessageAdapter:

    def __init__(self, conf_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        print(self.conf)

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

    def transform(self, recs):
        self.logger.info("Transform!")
        im_message = "A transformed message"

        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs

        evt_name = rec['eventName']
        evt_time = rec['eventTime']
        prc_id = rec['userIdentity']['principalId']

        im_message = ImMessage()
        pos = rec['s3']['object']['key'].rfind('/') + 1

        im_message.alg['algorithm'] = "MD5"
        # REVIEWME what to do if multipart upload
        im_message.alg_value['value'] = rec['s3']['object']['eTag']

        file_name = str(rec['s3']['object']['key'])[pos:]
        im_message.file_name['name'] = file_name
        im_message.file_size['size'] = rec['s3']['object']['size']
        im_message.file_format['format'] = self.conf['format']
        im_message.headers['headers'] = self.conf['headers']

        relationship = {}
        relationship['type'] = str(self.conf['type'])
        relationship['id'] = str(self.conf['collection_id'])
        im_message.append_relationship(relationship)

        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        s3_obj_uri = bucket + "/" + s3_key
        file_message = FileMessage(s3_obj_uri, "ARCHIVE", True, "Amazon:AWS:S3", False)

        im_message.set_file_locations(file_message)

        access_obj_uri = self.conf['access_bucket'] + "/" + rec['s3']['object']['key']
        file_message = FileMessage(access_obj_uri, "ACCESS", False, "HTTPS", False)
        # file_message.fl_lastMod['lastModified'] = TBD ISO conversion to millis

        im_message.set_file_locations(file_message)

        # Discovery block
        im_message.discovery['title'] = file_name
        im_message.discovery['parentIdentifier'] = self.conf['collection_id']
        im_message.discovery['fileIdentifier'] = "gov.noaa.ncei.csb:" + file_name[:-4]

        link = Link("download", "Amazon S3", "HTTPS", access_obj_uri)
        im_message.append_link_attributes(link)

        link = Link("download", "Amazon S3", "Amazon:AWS:S3", s3_obj_uri)
        im_message.append_link_attributes(link)

        payload = im_message.serialize()

        return payload
