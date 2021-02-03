
import yaml
from onestop.info.ImMessage import ImMessage
from onestop.info.FileMessage import FileMessage
from onestop.info.Link import Link
from onestop.util.ClientLogger import ClientLogger


class S3MessageAdapter:

    def __init__(self, conf_loc, s3_utils):
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)
        self.s3_utils = s3_utils

        self.prefix_mapping = {
            'NESDIS/CSB': '73d16fe3-7ccb-4918-b77f-30e343cdd378',
            'NESDIS/H8': '0fad03df-0805-434a-86a6-7dc42d68480e',
            'NESDIS/GOES': '11111111-1111-1111-1111-111111111111',
            'NESDIS/SAB': '98e03b47-069a-4f2c-8071-649e8c4254d6'
        }

    # Returns appropiate Collection ID with given s3_key
    def collection_id_map(self,s3_key):
        # Looks through our prefix map and returns appropiate collection id
        for key in self.prefix_mapping:
            if key in s3_key:
                return self.prefix_mapping[key]


    def transform(self, recs):
        self.logger.info("Transform!")
        im_message = None
        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs
        im_message = ImMessage()
        im_message.links = []

        s3_bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        print(s3_key)
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
                        'id': self.collection_id_map(s3_key)}
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

        # Discovery block
        im_message.discovery['title'] = file_name
        im_message.discovery['parentIdentifier'] = self.conf['collection_id']
        im_message.discovery['fileIdentifier'] = self.conf['file_identifier_prefix'] + file_name[:-4]


        https_link = Link("download", "Amazon S3", "HTTPS", access_obj_uri)
        im_message.append_link(https_link)

        s3_link = Link("download", "Amazon S3", "Amazon:AWS:S3", s3_obj_uri)
        im_message.append_link(s3_link)

        return im_message
