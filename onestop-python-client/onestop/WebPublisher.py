import logging
import requests
import yaml


class WebPublisher:
    conf = None

    def __init__(self, conf_loc, cred_loc):

        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        with open(cred_loc) as f:
            self.cred = yaml.load(f, Loader=yaml.FullLoader)

        self.setup_logger(self.__class__.__name__, False)
        self.logger.info("Initializing " + self.__class__.__name__)

    def setup_logger(self, log_name, create_file=False):

        # create logger
        self.logger = logging.getLogger(self.__class__.__name__)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.conf['log_level'] == "DEBUG":
            self.logger.setLevel(level=logging.DEBUG)
        else:
            if self.conf['log_level'] == "INFO":
                self.logger.setLevel(level=logging.INFO)
            else:
                self.logger.setLevel(level=logging.ERROR)

        fh = None
        if create_file:
            # create file handler for logger.
            fh = logging.FileHandler(log_name)
            fh.setFormatter(formatter)

        # create console handler for logger.
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # add handlers to logger.
        if create_file:
            self.logger.addHandler(fh)

        self.logger.addHandler(ch)

    def publish(self, metadata_type, uuid, payload):

        headers = {'Content-Type': 'application/json'}

        registry_url = self.conf['url'] + "/metadata/" + metadata_type + "/" + uuid
        print("Posting to: " + registry_url)
        response = requests.post(url=registry_url, headers=headers, auth=(self.cred['registry']['username'],
                                                                   self.cred['registry']['password']),
                          data=payload, verify=False)
        return response
