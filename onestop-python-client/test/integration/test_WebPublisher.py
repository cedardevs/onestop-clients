import yaml
import json
import unittest
import time
import os.path

from onestop.WebPublisher import WebPublisher
from os import path

class WebPublisherTest(unittest.TestCase):
    wp = None
    object_uuid = "7f0a5ff2-fcc0-5bcb-a225-024b669c9bba"
    collection_uuid = "fdb56230-87f4-49f2-ab83-104cfd073177"

    granule_payloadDict = {
        "fileInformation": {
                "name": "file2.csv",
                "size": 1385,
                "checksums": [{
                        "algorithm": "MD5",
                        "value": "44d2452e8bc2c8013e9c673086fbab7a"
                    }]
        },
        "relationships": [
            {"type": "COLLECTION",
             "id": collection_uuid
            }
        ],
        "fileLocations": {
            "nesdis-ncei-csb-dev/csv/file2.csv": {
                "uri": "https://odp-noaa-nesdis-ncei-test.s3-us-west-2.amazonaws.com/csv/file2.csv",
                "type": "ACCESS",
                "restricted": False,
                "serviceType": "HTTPS",
                "asynchronous": False
            }
        },
        "discovery": {
            "title": "file2.csv",
            "parentIdentifier": collection_uuid,
            "fileIdentifier": "gov.noaa.ncei.csb:file2"
        }
    }

    addlocDict = {
        "fileLocations": {
            "Crt3a-Hq2SGUp8n8QSRNpFIf59kmMONqaKlJ_7-Igd8ijMM62deLdtVkiYwlaePbC4JNCsfeg5i-DWDmwxLIx9V-OGgiQp_CZ0rEFXIZxM_ZPyGu7TTv8wwos5SvAI6xDURhzoCH-w": {
                "uri": "/282856304593/vaults/noaa-nesdis-ncei-vault-test/archives/Crt3a-Hq2SGUp8n8QSRNpFIf59kmMONqaKlJ_7-Igd8ijMM62deLdtVkiYwlaePbC4JNCsfeg5i-DWDmwxLIx9V-OGgiQp_CZ0rEFXIZxM_ZPyGu7TTv8wwos5SvAI6xDURhzoCH-w",
                "type": "ACCESS",
                "restricted": True,
                "serviceType": "Amazon:AWS:Glacier",
                "asynchronous": True
            }
        }
    }

    @classmethod
    def setUpClass(cls):
        print("Set it up!")

        cred_loc = "config/credentials.yml"
        conf_loc = "config/csb-data-stream-config-template.yml"

        if path.exists(cred_loc):
            with open(cred_loc) as f:
                creds = yaml.load(f, Loader=yaml.FullLoader)

            registry_username = creds['registry']['username']
            registry_password = creds['registry']['password']
            access_key = creds['sandbox']['access_key']
            access_secret = creds['sandbox']['secret_key']
        else:
            print("Credentials file doesn't exist at '%s', using environment variables."%cred_loc)
            registry_username = os.environ.get('REGISTRY_USERNAME')
            registry_password = os.environ.get("REGISTRY_PASSWORD")
            access_key = os.environ.get("ACCESS_KEY")
            access_secret = os.environ.get("SECRET_KEY")
            if registry_username == None:
                msg = "REGISTRY_USERNAME not defined as env variable. Credentials file at '" + cred_loc + "' doesn't exist."
                raise Exception(msg)

        with open(conf_loc) as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)

        registry_base_url = conf['registry_base_url']
        onestop_base_url = conf['onestop_base_url']

        config_dict = {
            "registry_username": registry_username,
            "registry_password": registry_password,
            "access_key": access_key,
            "access_secret": access_secret,
            "registry_base_url": registry_base_url,
            "onestop_base_url": onestop_base_url,
            "log_level":"DEBUG"
        }

        cls.wp = WebPublisher(**config_dict)

    @classmethod
    def tearDownClass(cls):
        print("Tear it down!")
        cls.wp.delete_registry("granule", cls.object_uuid)

    def test_publish_get_delete_granule_registry_onestop(self):
        print("test_publish_get_delete_granule")

        print("Cleanup from prior test runs: Waiting for granule to be deleted in Registry and OneStop")
        self.wp.delete_registry("granule", self.object_uuid)
        secondsWait = 150
        self.assertTrue(self.wait_until(lambda: (self.get_onestop_granule_count(self.collection_uuid) == 0), secondsWait, 10),
                        "Waited "+str(secondsWait)+" seconds for OneStop to delete granule(s) with collection id="+self.collection_uuid)

        # Publish to Registry
        payload = json.dumps(self.granule_payloadDict)
        response = self.wp.publish_registry("granule", self.object_uuid, payload, "POST")
        self.assertTrue(response, "Failed to publish granule to registry")
        response = self.wp.search_registry("granule", self.object_uuid)
        self.assertTrue(response, "Failed to search for granule in Registry")

        print("Waiting for granules to be searchable in OneStop")
        secondsWait = 150
        self.assertTrue(self.wait_until(lambda: (self.get_onestop_granule_count(self.collection_uuid) > 0), secondsWait, 10),
                        "Waited "+str(secondsWait)+" seconds for OneStop to have the granule with collection id="+self.collection_uuid)

        response = self.wp.delete_registry("granule", self.object_uuid)
        self.assertTrue(response, "Failed to delete granule from registry")

        print("Waiting for granule to be deleted in OneStop")
        secondsWait = 150
        self.assertTrue(self.wait_until(lambda: (self.get_onestop_granule_count(self.collection_uuid) == 0), secondsWait, 10),
                        "Waited "+str(secondsWait)+" seconds for OneStop to delete granule(s) with collection id="+self.collection_uuid)

    def test_add_glacier_location(self):
        payload = json.dumps(self.addlocDict)
        response = self.wp.publish_registry("granule", self.object_uuid, payload, "PATCH")
        self.assertTrue(response)

    def wait_until(self, somepredicate, timeout, period=0.25, *args, **kwargs):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if somepredicate(*args, **kwargs):
                return True

            print("Waiting "+str(period)+" seconds for condition to be true.")
            time.sleep(period)
        return False

    def get_onestop_granule_count(self, collection_uuid):
        response = self.wp.get_granules_onestop(collection_uuid)
        response_dict = json.loads(response.text)
        data_list = response_dict['data']
        print("OneStop granule count for collection_uuid "+collection_uuid+" is "+str(data_list.__len__()))

        return data_list.__len__()

if __name__ == '__main__':
    unittest.main()