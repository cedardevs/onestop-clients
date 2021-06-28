from onestop.util.ClientLogger import ClientLogger

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.parsed_record import ParsedRecord, Publishing, ErrorEvent
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_location import FileLocation,FileLocationType
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.file_information import FileInformation
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.checksum import Checksum, ChecksumAlgorithm
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.relationship import Relationship
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.discovery import Discovery, Link


class S3MessageAdapter:
    """
    A class used to extract information from sqs messages that have been triggered by s3 events and transform it into correct format for publishing to IM Registry

    Attributes
    ----------
        access_bucket: str
            Cloud bucket to put in the links field when transformed.
        type: str
            COLLECTION or GRANULE
        file_id_prefix: str
            File prefix returned as fileIdentifier
        collection_id: str
            Collection this data belongs to. Returned as parent identifier.
        log_level: str
            The log level to use for this class (Defaults to 'INFO')

        logger: ClientLogger object
            utilizes python logger library and creates logging for our specific needs
        logger.info: ClientLogger object
            logging statement that occurs when the class is instantiated

    Methods
    -------
        transform(recs)
            transforms sqs message triggered by s3 event to correct format for publishing to IM registry
    """
    def __init__(self,  access_bucket, s3_message_adapter_metadata_type, file_id_prefix, collection_id, log_level = 'INFO', **wildargs):
        """
        Parameters
        ----------
        access_bucket: str
            access bucket to put in the links field when transformed.
        s3_message_adapter_metadata_type: str
            COLLECTION or GRANULE
        file_id_prefix: str
            File prefix returned as fileIdentifier
        collection_id: str
            Collection this data belongs to. Returned as parent identifier.
        log_level: str
            Log level for when logging in class.

        """
        self.access_bucket = access_bucket
        self.metadata_type = s3_message_adapter_metadata_type.upper()
        self.file_id_prefix = file_id_prefix
        self.collection_id = collection_id
        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
        self.logger.info("Initializing " + self.__class__.__name__)

        if self.metadata_type not in ['COLLECTION', 'GRANULE']:
            raise ValueError("metadata_type of '%s' must be 'COLLECTION' or 'GRANULE'"%(self.metadata_type))

        if wildargs:
            self.logger.debug("Superfluous parameters in constructor call: " + str(wildargs))

    def transform(self, recs):
        """
        Transforms sqs message triggered by s3 event to correct format for publishing to IM registry

        Parameters:
        ----------
        recs: dict
            sqs event message to transform

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
        relationship = Relationship(id=self.collection_id, type=self.metadata_type)

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
        access_obj_uri = self.access_bucket + "/" + s3_key
        link1 = Link(linkName="Amazon S3", linkUrl=access_obj_uri, linkProtocol="HTTPS", linkFunction="download")
        link2 = Link(linkName="Amazon S3", linkUrl=s3_obj_uri, linkProtocol="Amazon:AWS:S3", linkFunction="download")
        # To Change? Come back to this later
        parent_identifier = self.collection_id
        file_identifier = self.file_id_prefix + file_name[:-4]

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

