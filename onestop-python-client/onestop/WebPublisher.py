import logging
import requests
import yaml
from onestop.util.ClientLogger import ClientLogger

class WebPublisher:
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.logger = ClientLogger.get_logger(self.__class__.__name__, self.conf['log_level'], False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def publish_registry(self, metadata_type, uuid, payload):

        headers = {'Content-Type': 'application/json'}

        registry_url = self.conf['registry_base_url'] + "/metadata/" + metadata_type + "/" + uuid
        print("Post: " + registry_url)
        response = requests.post(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                   self.cred['registry']['password']),
                          data=payload, verify=False)
        return response

    def delete_registry(self, metadata_type, uuid):

        headers = {'Content-Type': 'application/json'}

        registry_url = self.conf['registry_base_url'] + "/metadata/" + metadata_type + "/" + uuid
        print("Delete: " + registry_url)
        response = requests.delete(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                            self.cred['registry']['password']), verify=False)
        return response

    def consume_registry(self, metadata_type, uuid):

        headers = {'Content-Type': 'application/json'}

        registry_url = self.conf['registry_base_url'] + "/metadata/" + metadata_type + "/" + uuid
        print("Get: " + registry_url)
        response = requests.get(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                         self.cred['registry']['password']), verify=False)
        return response

    def get_granules_onestop(self, metadata_type, uuid):

        # url = 'https://ab76afcf90ee844ea95ba43a75c3624c-1204932138.us-east-1.elb.amazonaws.com/onestop-search/search/granule'
        payload = '{"queries":[],"filters":[{"type":"collection","values":["' + uuid +  '"]}],"facets":true,"page":{"max":50,"offset":0}}'

        headers = {'Content-Type': 'application/json'}
        onestop_url = self.conf['onestop_base_url'] + "/" + metadata_type

        print("Get: " + onestop_url)
        response = requests.get(url=onestop_url, headers=headers, data=payload, verify=False)
        return response
