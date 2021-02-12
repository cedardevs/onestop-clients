import yaml
from onestop.util.ClientLogger import ClientLogger

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord, Publishing, ErrorEvent
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location import FileLocation,FileLocationType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_information import FileInformation
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum import Checksum, ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship import Relationship, RelationshipType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.discovery import Discovery, Link

class S3MessageAdapter:

    def __init__(self, conf_loc, s3_utils):
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)
        self.s3_utils = s3_utils

        self.prefix_mapping = self.conf['prefixMap']

    # Returns appropiate Collection ID with given s3_key
    def collection_id_map(self,s3_key):
        # Looks through our prefix map and returns appropiate collection id
        for key in self.prefix_mapping:
            if key in s3_key:
                return self.prefix_mapping[key]


    def transform(self, recs):
        print('Hello-------------------------')
        self.logger.info("Transform!")
        print('In Transfrom')
        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs

        s3_bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        pos = s3_key.rfind('/') + 1

        checkSumAlgorithm = ChecksumAlgorithm(value='MD5')
        alg_value = rec['s3']['object']['eTag']
        checkSum = Checksum(algorithm=checkSumAlgorithm, value=alg_value)
        checkSum_dict = checkSum.to_dict()

        file_name = str(s3_key)[pos:]
        file_size = rec['s3']['object']['size']
        fileInformation = FileInformation(name=file_name, size=file_size, checksums=[checkSum], optionalAttributes={})

        # Relationship
        relationshipType = RelationshipType(type=self.conf['type'])
        relationship = Relationship(id=self.conf['collection_id'], type=relationshipType)

        # File Location
        fileLocationType = FileLocationType(type='ARCHIVE')
        s3_obj_uri = "s3://" + s3_bucket + "/" + s3_key
        fileLocation = FileLocation(uri=s3_obj_uri, type=fileLocationType, deleted=False, restricted=True,
                                    asynchronous=False, serviceType='Amazon:AWS:S3')

        # Error Event
        errorEvent = ErrorEvent()

        # Publishing
        publishing = Publishing(isPrivate=True)

        # Discovery
        access_obj_uri = self.conf['access_bucket'] + "/" + s3_key
        link1 = Link(linkName="Amazon S3", linkUrl=access_obj_uri, linkProtocol="HTTPS", linkFunction="download")
        link2 = Link(linkName="Amazon S3", linkUrl=s3_obj_uri, linkProtocol="Amazon:AWS:S3", linkFunction="download")
        # To Change? Come back to this later
        parent_identifier = self.conf['collection_id']
        file_identifier = self.conf['file_identifier_prefix'] + file_name[:-4]

        discovery = Discovery(links=[link1, link2], title=file_name, parentIdentifier=parent_identifier,
                              fileIdentifier=file_identifier)

        parsedRecord = ParsedRecord(fileInformation=fileInformation, fileLocations=fileLocation,
                                    relationships=[relationship], errors=[errorEvent], publishing=publishing,
                                    discovery=discovery)
        print('Parsed Record Discover', parsedRecord.discovery)
        # Return parsedRecord object
        return parsedRecord

        """
        self.logger.info("Transform!")
        im_message = None
        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs
        print('S3MA recs', rec)
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
        self.logger.info('S3 URI: ' + str(s3_obj_uri))
        file_message = FileMessage(s3_obj_uri, "ARCHIVE", True, "Amazon:AWS:S3", False)

        im_message.append_file_message(file_message)

        access_obj_uri = self.conf['access_bucket'] + "/" + s3_key
        self.logger.info('Access Object uri: ' + str(access_obj_uri))

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
        """

