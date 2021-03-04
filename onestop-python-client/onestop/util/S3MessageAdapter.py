from onestop.info.ImMessage import ImMessage
from onestop.info.FileMessage import FileMessage
from onestop.info.Link import Link
from onestop.util.ClientLogger import ClientLogger


class S3MessageAdapter:

    def __init__(self,  access_bucket, prefix_mapping, format, headers, type, file_id_prefix, log_level = 'INFO'):
        self.access_bucket = access_bucket
        self.prefix_map = prefix_mapping
        self.format = format
        self.headers = headers
        self.type = type
        self.file_id_prefix = file_id_prefix
        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
        self.logger.info("Initializing " + self.__class__.__name__)

        self.prefix_mapping = prefix_mapping

    # Returns appropiate Collection ID with given s3_key
    def collection_id_map(self,s3_key):
        # Looks through our prefix map and returns appropiate collection id
        for key in self.prefix_mapping:
            if key in s3_key:
                return self.prefix_mapping[key]


    #TODO fix the bucket overrides to support copy after demo!
    def transform(self, recs, s3_bucket = None, access_bucket = None):
        self.logger.info("Transform!")
        im_message = None
        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs
        im_message = ImMessage()
        im_message.links = []

        self.logger.info("Transform from bucket: " + rec['s3']['bucket']['name'])
        buckettest = s3_bucket if None else "Same"
        self.logger.info("Transform to bucket: " + buckettest)
        s3_bucket = s3_bucket if None else rec['s3']['bucket']['name']

        s3_key = rec['s3']['object']['key']
        print(s3_key)
        pos = s3_key.rfind('/') + 1

        im_message.alg = "MD5"  # or perhaps Etag
        # # REVIEW  ME what to do if multipart upload
        im_message.alg_value = rec['s3']['object']['eTag']

        file_name = str(s3_key)[pos:]
        im_message.file_name = file_name
        im_message.file_size = rec['s3']['object']['size']
        im_message.file_format = self.format
        im_message.headers = self.headers
        parent_id = self.collection_id_map(s3_key)

        self.logger.info("Associating granule with " + parent_id)
        relationship = {'type': str( type ),
                        'id': parent_id}
        im_message.append_relationship(relationship)

        s3_obj_uri = "s3://" + s3_bucket + "/" + s3_key
        self.logger.info('S3 URI: ' + str(s3_obj_uri))
        file_message = FileMessage(s3_obj_uri, "ARCHIVE", True, "Amazon:AWS:S3", False)

        im_message.append_file_message(file_message)
        bucket = access_bucket if None else self.access_bucket
        access_obj_uri = bucket + "/" + s3_key
        self.logger.info('Access Object uri: ' + str(access_obj_uri))

        file_message = FileMessage(access_obj_uri, "ACCESS", False, "HTTPS", False)

        # file_message.fl_lastMod['lastModified'] = TBD ISO conversion to millis

        im_message.append_file_message(file_message)

        # Discovery block
        im_message.discovery['title'] = file_name
        im_message.discovery['parentIdentifier'] = parent_id
        im_message.discovery['fileIdentifier'] = self.file_id_prefix + file_name[:-4]

        https_link = Link("download", "Amazon S3", "HTTPS", access_obj_uri)
        im_message.append_link(https_link)

        s3_link = Link("download", "Amazon S3", "Amazon:AWS:S3", s3_obj_uri)
        im_message.append_link(s3_link)

        return im_message
