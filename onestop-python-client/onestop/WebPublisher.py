import logging
import requests
import urllib3
import yaml
from onestop.util.ClientLogger import ClientLogger

class WebPublisher:
    conf = None

    def __init__(self, registry_base_url, username = None, password = None, log_level = 'INFO'):
        self.registry_base_url = registry_base_url
        self.username = username
        self.password = password
        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def publish_registry(self, metadata_type, uuid, payload, method):
        #TODO symptom of cert issues, fix me later
        urllib3.disable_warnings()
        headers = {'Content-Type': 'application/json'}
        registry_url = self.registry_base_url + "/metadata/" + metadata_type + "/" + uuid
        self.logger.info("Sending " +  method + " for " + metadata_type + " with ID " + uuid + " to " + registry_url)
        if method == "POST":
            response = requests.post(url=registry_url, headers=headers, auth=(self.username,
                                                                       self.password),
                              data=payload, verify=False)

        if method == "PATCH":
            response = requests.patch(url=registry_url, headers=headers, auth=(self.username,
                                                                       self.password),
                              data=payload, verify=False)

        if method == "PUT":
            response = requests.put(url=registry_url, headers=headers, auth=(self.username,
                                                                       self.password),
                              data=payload, verify=False)
        return response

    def delete_registry(self, metadata_type, uuid):
        self.logger.info("Deleting " + metadata_type + " with id : " + uuid)
        headers = {'Content-Type': 'application/json'}
        registry_url = self.registry_base_url + "/metadata/" + metadata_type + "/" + uuid
        self.logger.info("Sending DELETE by ID to: " + registry_url)
        response = requests.delete(url=registry_url, headers=headers, auth=(self.username,
                                                                            self.password), verify=False)
        self.logger.info(response)
        return response

    def consume_registry(self, metadata_type, uuid):
        self.logger.info("Fetching record by id: " + uuid)
        headers = {'Content-Type': 'application/json'}
        registry_url = self.registry_base_url + "/metadata/" + metadata_type + "/" + uuid
        self.logger.info("Sending GET by id to: " + registry_url)
        response = requests.get(url=registry_url, headers=headers, auth=(self.username,
                                                                         self.password), verify=False)
        self.logger.info(response)
        return response

    def search_onestop(self, metadata_type, payload):
        self.logger.info("Searching for " + metadata_type )
        self.logger.info("Payload: " + payload)
        headers = {'Content-Type': 'application/json'}
        onestop_url = self.conf['onestop_base_url'] + "/search/" + metadata_type
        self.logger.info("Sending search (POST) to: " + onestop_url)
        response = requests.get(url=onestop_url, headers=headers, data=payload, verify=False)
        self.logger.info(response.json())
        return response

    def get_granules_onestop(self, metadata_type, uuid):
        self.logger.info("Fetching " + metadata_type + " for id: " + uuid)
        payload = '{"queries":[],"filters":[{"type":"collection","values":["' + uuid +  '"]}],"facets":true,"page":{"max":50,"offset":0}}'

        self.search_onestop(metadata_type, payload)
