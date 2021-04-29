import json


class DataLakeMessage:

    def __init__(self):
        self.file_name = None
        self.file_size = None
        self.alg = None
        self.alg_value = None
        self.chk_sums = [{"algorithm": None, "value": None}]
        self.file_format = "None"

        self.headers = None
        self.optAttrFileInfo = None

                # Relationships
        self.relationships = []
        self.parentUuid = ""
        #self.parentDoi = ""
        self.rel_type = ""

        self.uri = ""
        self.type = ""
        self.deleted = False
        self.restricted = False
        self.asynchronous = False
        self.locality = None
        self.lastModifiedMillis = None
        self.service_type = ""               
        self.optAttrFileLoc = ""
        # Discovery
        self.fileIdentifier = None
        self.discovery = {}
        self.links = []
        self.spatialBounding = {}
        self.coordinates= []
        self.begin_dt = None
        self.end_dt = None
        self.begin_date_str = ""
        self.end_date_str = ""
        self.temporalBounding = {}
        self.parentIdentifier = None
        self.keywords = []

        #this is only used for NOAA object tagging, not in onestop payload
        self.s3Bucket = None
        self.s3Key = None
        self.S3Dir = None
        # Record
        self.file_messages = []

    def append_file_message(self, file_message):
        self.file_messages.append(file_message)

    def append_link(self, link):
        self.links.append(link)

    def append_relationship(self, relationship):
        self.relationships.append(relationship)

    def serialize(self):
        payload = {}
        file_locations = {}
        file_locations[self.uri] = {
            "uri": self.uri,
            "type": self.type,
            "deleted": self.deleted,
            "restricted": self.restricted,
            "asynchronous": self.asynchronous,
            "locality": self.locality,
            "lastModified": self.lastModifiedMillis,
            "serviceType": self.service_type,
            "optionalAttributes":self.optAttrFileLoc
        }
        payload["fileLocations"] = file_locations

        

        self.chk_sums = [{"algorithm": self.alg, "value": self.alg_value}]
        file_information = {"name": self.file_name, 
            "size": self.file_size,
            "checksums": self.chk_sums,
            "format": self.file_format,
            "headers":self.headers,
            "optionalAttributes": self.optAttrFileInfo}

        payload['fileInformation'] = file_information

        #set in GefsExtractor.createMetadataMessage()
        relationship ={
            "id":self.parentUuid,
            "type":self.rel_type
        }
        self.append_relationship(relationship)
        payload['relationships'] = self.relationships
        file_location = {}

        payload['fileLocations'] = file_locations

        link_list = []
        for link in self.links:
            link_list.append({
                "linkName": link.name,
                "linkUrl": link.url,
                "linkProtocol": link.protocol,
                "linkFunction": link.function
            })

        self.spatialBounding = {
                    "type": "Polygon",
                    "coordinates": self.coordinates}

      
        self.temporalBounding = {
            "beginDate": self.begin_date_str,
            "endDate": self.end_date_str
        }
        discovery = {
            "title": self.file_name,
            "fileIdentifier": self.fileIdentifier,
            "links": link_list, 
            "parentIdentifier": self.parentIdentifier,
            "spatialBounding": self.spatialBounding, 
            "temporalBounding": self.temporalBounding,
            "keywords":self.keywords}
        payload["discovery"] = discovery
        #json_payload = json.dumps(payload, indent=2)

        # Return
        return payload
