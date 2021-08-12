import yaml
from onestop.util.ClientLogger import ClientLogger
"""
from onestop.info.ImMessage import ImMessage
from onestop.info.FileMessage import FileMessage
from onestop.info.Link import Link
"""

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord, Publishing, ErrorEvent
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location import FileLocation,FileLocationType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_information import FileInformation
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum import Checksum, ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship import Relationship, RelationshipType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.discovery import Discovery, Link



class S3MessageAdapter:
    """
    A class used to extract information from sqs messages that have been triggered by s3 events and transform it into correct format for publishing to IM Registry

    Attributes
    ----------
    conf: yaml file
        csb-data-stream-config.yml
    s3_utils: S3Utils object
        used to access objects inside of s3 buckets
    logger: ClientLogger object
        utilizes python logger library and creates logging for our specific needs
    logger.info: ClientLogger object
        logging statement that occurs when the class is instantiated
    prefix_mapping: Dict
        contains mapping of various line offices and their associated collection id

    Methods
    -------
    collection_id_map(s3_key)
        given an s3 key that contains one of the NESDIS line offices in its path, it will provide the corresponding collection id

    transform(recs)
        transforms sqs message triggered by s3 event to correct format for publishing to IM registry
    """
    def __init__(self, conf_loc, s3_utils):
        """

        :param conf_loc: yaml file
            csb-data-stream-config.yml
        :param s3_utils: S3Utils object
            used to access objects inside of s3 buckets

        Other Attributes
        ----------------
        logger: ClientLogger object
            utilizes python logger library and creates logging for our specific needs
        logger.info: ClientLogger object
            logging statement that occurs when the class is instantiated
        prefix_mapping: Dict
            contains mapping of various line offices and their associated collection id

        """
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)
        self.s3_utils = s3_utils

        self.prefix_mapping = self.conf['prefixMap']

    def collection_id_map(self, s3_key):
        """
        Given an s3 key that contains one of the NESDIS line offices in its path, it will provide the corresponding collection id

        :param s3_key: str
            key path of object in s3 bucket

        :return: str
            associated line office collection id
        """
        # Looks through our prefix map and returns appropriate collection id
        for key in self.prefix_mapping:
            if key in s3_key:
                return self.prefix_mapping[key]


    def transform(self, recs):
        """
        Transforms sqs message triggered by s3 event to correct format for publishing to IM registry

        :param recs: dict
            sqs event message

        :return: ParsedRecord Object
            The Parsed Record class is an avro schema generated class
        """

        self.logger.info("Transform!")
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
                                    asynchronous=False, serviceType='Amazon:AWS:S3', optionalAttributes={})

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

        # Initializing most fields to their default values in the avro schema so that it doesn't cause an error in Kafka
        discovery = Discovery(links=[link1, link2], title=file_name, parentIdentifier=parent_identifier,
                              fileIdentifier=file_identifier, keywords=[], topicCategories=[], acquisitionInstruments=[], acquisitionOperations=[],
                              acquisitionPlatforms=[], dataFormats=[], responsibleParties=[], citeAsStatements=[], crossReferences=[], largerWorks=[],
                              legalConstraints=[], dsmmAccessibility=0, dsmmDataIntegrity=0, dsmmDataQualityAssessment=0, dsmmDataQualityAssurance=0,
                              dsmmDataQualityControlMonitoring=0, dsmmPreservability=0, dsmmProductionSustainability=0, dsmmTransparencyTraceability=0,
                              dsmmUsability=0, dsmmAverage=0.0, services=[])

        parsedRecord = ParsedRecord(fileInformation=fileInformation, fileLocations=fileLocation,
                                    relationships=[relationship], errors=[errorEvent], publishing=publishing,
                                    discovery=discovery)
        # Return parsedRecord object
        return parsedRecord

