import json


class ImMessage:

    def __init__(self):
        # File Information
        self.file_name = None
        self.file_size = None
        self.alg = None
        self.alg_value = None
        self.chk_sums = [{"algorithm": None, "value": None}]
        self.file_format = None
        self.headers = None

        # Relationships
        self.relationships = []

        # Discovery
        self.discovery = {}
        self.links = []
        self.spatialBounding = None
        self.coordinates= None
        self.temporalBounding = {}
        self.parentIdentifier = {"parentIdentifier": None}

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
        for fm in self.file_messages:
            file_locations[fm.uri] = {
                    "uri": fm.uri,
                    "type": fm.type,
                    "restricted": fm.restricted,
                    "serviceType": fm.service_type,
                    "asynchronous": fm.asynchronous
                }


        chk_sums = [{"algorithm": self.alg, "value": self.alg_value}]
        file_information = {"name": self.file_name, "size": self.file_size, "checksums": chk_sums}

        payload['fileInformation'] = file_information
        payload['relationships'] = self.relationships

        payload['fileLocations'] = file_locations

        link_list = []
        for link in self.links:
            link_list.append({
                "linkName": link.name,
                "linkUrl": link.url,
                "linkProtocol": link.protocol,
                "linkFunction": link.function
            })

        self.spatialBounding = {'coordinates': self.coordinates} if self.coordinates is not None else None
        discovery = {'links': link_list, 'spatialBounding': self.spatialBounding, 'temporalBounding': self.temporalBounding}
        payload['discovery'] = discovery
        json_payload = json.dumps(payload, indent=2)

        # Return
        return json_payload
