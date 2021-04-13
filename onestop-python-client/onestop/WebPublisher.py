import requests
import yaml
from onestop.util.ClientLogger import ClientLogger

class WebPublisher:
    """
    A class to publish to registry through https

    Attributes
    ----------
    registry_base_url: str
        url for registry endpoint
    registry_username: str
        username for posting metadata to registry
    registry_password: str
        password for posting metadata to registry
    onestop_base_url: str
        url for onestop endpoint
    logger.info: str
        logging level

    Methods
    -------
    publish_registry(metadata_type, uuid, payload, method)
        publish to registry with either POST,PUT, OR PATCH methods

    """
    conf = None

    def __init__(self, registry_base_url, registry_username, registry_password, onestop_base_url, log_level="INFO", **kwargs):
        self.registry_base_url = registry_base_url
        self.registry_username = registry_username
        self.registry_password = registry_password
        self.onestop_base_url = onestop_base_url
        self.logger = ClientLogger.get_logger(self.__class__.__name__, log_level, False)
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
        registry_url = self.registry_base_url + "/metadata/" + metadata_type + "/" + uuid
        self.logger.info("Sending WP a " + method + " for " + metadata_type + " with ID " + uuid + " to " + registry_url)
        self.logger.info("Payload:" + payload)
        if method == "POST":
            response = requests.post(url=registry_url, headers=headers, auth=(self.registry_username,
                                                                       self.registry_password),
                              data=payload, verify=False)

        if method == "PATCH":
            response = requests.patch(url=registry_url, headers=headers, auth=(self.registry_username,
                                                                       self.registry_password),
                              data=payload, verify=False)

        if method == "PUT":
            response = requests.put(url=registry_url, headers=headers, auth=(self.registry_username,
                                                                       self.registry_password),
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
        registry_url = self.registry_base_url + "/metadata/" + metadata_type + "/" + uuid
        self.logger.info("Sending DELETE by ID to: " + registry_url)
        response = requests.delete(url=registry_url, headers=headers, auth=(self.registry_username,
                                                                            self.registry_password), verify=False)
        self.logger.info(response)
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
        onestop_url = self.onestop_base_url + "/" + metadata_type

        print("Search: " + onestop_url)
        response = requests.get(url=onestop_url, headers=headers, data=payload, verify=False)
        return response

    def get_granules_onestop(self, uuid):
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

        response = self.search_onestop("granule", payload)
        self.logger.info( response )
        return response
