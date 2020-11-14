import json


class ImMessage:

    def __init__(self):
        # File Information
        self.file_name = {"name": None}
        self.file_size = {"size": None}
        self.alg = {"algorithm": None}
        self.alg_value = {"value": None}
        self.chk_sums = {"checksums": [self.alg, self.alg_value]}
        self.file_format = {"format": None}
        self.headers = {"headers": None}

        # Relationships
        self.relationships = []

        # Discovery
        self.discovery = {}
        self.links = []
        self.parentIdentifier = {"parentIdentifier": None}

        # Record
        self.file_information = [self.file_name, self.file_size, self.chk_sums, self.file_format, self.headers]
        self.file_messages = []
        self.file_locations = {}

    def append_file_message(self, file_message):
        self.file_messages.append(file_message)

    def append_link(self, link):
        self.links.append(link)

    def append_relationship(self, relationship):
        self.relationships.append(relationship)

    def serialize(self):
        payload = {}
        file_message_list = []

        for fm in self.file_messages:
            file_message_list.append({
                "uri": fm.uri,
                "type": fm.type,
                "restricted": fm.restricted,
                "serviceType": fm.service_type,
                "asynchronous": fm.asynchronous
            })

        payload['fileInformation'] = self.file_information
        payload['relationships'] = self.relationships

        payload['fileLocations'] = file_message_list

        link_list = []
        for link in self.links:
            link_list.append({
                "linkName": link.name,
                "linkUrl": link.url,
                "linkProtocol": link.protocol,
                "linkFunction": link.function
            })

        discovery = {'links': link_list}
        payload['discovery'] = discovery
        json_payload = json.dumps(payload, indent=2)

        # Return
        return json_payload
