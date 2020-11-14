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

        registry_url = self.conf['url'] + "/metadata/" + metadata_type + "/" + uuid
        print("Posting to: " + registry_url)
        response = requests.post(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                   self.cred['registry']['password']),
                          data=payload, verify=False)
        return response
