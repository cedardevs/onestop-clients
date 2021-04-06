import logging
import requests
import urllib3
import yaml
from onestop.util.ClientLogger import ClientLogger

class WebPublisher:
    """
    A class to publish to registry through https

    Attributes
    ----------
    conf_loc: yaml file
        web-publisher-config-dev.yml
    cred_loc: yaml file
        credentials.yml
    logger: ClientLogger object
            utilizes python logger library and creates logging for our specific needs
    logger.info: ClientLogger object
        logging statement that occurs when the class is instantiated

    Methods
    -------
    publish_registry(metadata_type, uuid, payload, method)
        publish to registry with either POST,PUT, OR PATCH methods

    """
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def publish_registry(self, metadata_type, uuid, payload, method):
        """
        Publish to registry with either POST,PUT, OR PATCH methods

        :param metadata_type: str
            metadata type (GRANULE/COLLECTION)
        :param uuid: str
            uuid you want to publish with
        :param payload: dict
            information you want to publish
        :param method: str
            POST,PUT,PATCH

        :return: str
            response message telling if the request was successful
        """
        headers = {'Content-Type': 'application/json'}
        registry_url = self.conf['registry_base_url'] + "/metadata/" + metadata_type + "/" + uuid
        self.logger.info("Posting " + metadata_type + " with ID " + uuid + " to " + registry_url)
        if method == "POST":
            response = requests.post(url=registry_url, headers=headers,auth=(self.cred['registry']['username'],
                                                                       self.cred['registry']['password']),
                              data=payload, verify=False)

        if method == "PATCH":
            response = requests.patch(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                       self.cred['registry']['password']),
                              data=payload, verify=False)

        if method == "PUT":
            response = requests.put(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                       self.cred['registry']['password']),
                              data=payload, verify=False)
        return response

    def delete_registry(self, metadata_type, uuid):
        """
        Deletes item from registry

        :param metadata_type: str
            metadata type (GRANULE/COLLECTION)
        :param uuid: str
            uuid you want to publish with

        :return: str
            response message indicating if delete was successful
        """

        headers = {'Content-Type': 'application/json'}

        registry_url = self.conf['registry_base_url'] + "/metadata/" + metadata_type + "/" + uuid
        print("Delete: " + registry_url)
        response = requests.delete(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                            self.cred['registry']['password']), verify=False)
        return response

    def consume_registry(self, metadata_type, uuid):
        """
        Acquires information of an item in registry given its metadata type and uuid

        :param metadata_type: str
            metadata type (GRANULE/COLLECTION)
        :param uuid: str
            uuid you want to publish with

        :return: str
            contents of the item in registry if the response was successful
        """
        headers = {'Content-Type': 'application/json'}

        registry_url = self.conf['registry_base_url'] + "/metadata/" + metadata_type + "/" + uuid
        print("Get: " + registry_url)
        response = requests.get(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                         self.cred['registry']['password']), verify=False)
        return response

    def search_onestop(self, metadata_type, payload):
        """
        Checks to see if the item is in onestop

        :param metadata_type: str
            metadata type (GRANULE/COLLECTION)
        :param payload: dict
            contents of the item

        :return: str
            response message indicating if request was successful
        """
        headers = {'Content-Type': 'application/json'}
        onestop_url = self.conf['onestop_base_url'] + "/" + metadata_type

        print("Get: " + onestop_url)
        response = requests.get(url=onestop_url, headers=headers, data=payload, verify=False)
        return response

    def get_granules_onestop(self, metadata_type, uuid):
        """
        Acquires granules from onestop given metadata type and uuid

        :param metadata_type: str
            metadata type (GRANULE/COLLECTION)
        :param uuid: str
            uuid you want to publish with

        :return: str
            response message indicating if request was successful
        """
        payload = '{"queries":[],"filters":[{"type":"collection","values":["' + uuid +  '"]}],"facets":true,"page":{"max":50,"offset":0}}'

        self.search_onestop(metadata_type, payload)
