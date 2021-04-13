import yaml
import json
import unittest

from onestop.WebPublisher import WebPublisher

class WebPublisherTest(unittest.TestCase):
    wp = None
    object_uuid = "9f0a5ff2-fcc0-5bcb-a225-024b669c9bba"
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
             "id": "fdb56230-87f4-49f2-ab83-104cfd073177"
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
            "parentIdentifier": "fdb56230-87f4-49f2-ab83-104cfd073177",
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

        cred_loc = "../config/credentials.yml"
        conf_loc = "../config/csb-data-stream-config-template.yml"

        with open(cred_loc) as f:
            creds = yaml.load(f, Loader=yaml.FullLoader)

        registry_username = creds['registry']['username']
        registry_password = creds['registry']['password']
        access_key = creds['sandbox']['access_key']
        access_secret = creds['sandbox']['secret_key']

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
            "onestop_base_url": onestop_base_url
        }

        cls.wp = WebPublisher(config_dict)

    @classmethod
    def tearDownClass(cls):
        print("Tear it down!")

    def test_publish_granule(self):
        payload = json.dumps(self.granule_payloadDict)
        response = self.wp.publish_registry("granule", self.object_uuid, payload, "POST")
        print (response.json())

    def test_get_granules(self):
        response = self.wp.get_granules_onestop(self.collection_uuid)
        print(response.json())

    def test_delete_granule(self):
        response = self.wp.delete_registry("granule", self.object_uuid)
        print(response.json())

    def test_delete_granules(self):
        response = self.wp.get_granules_onestop(self.collection_uuid)
        print(response.json())
        response_dict = json.loads(response.text)
        # items = response.json().items()
        data_list = response_dict['data']
        # print (str(data_list))
        for item in data_list:
            uuid = item['id']
            self.wp.delete_registry( "granule", uuid)

    def test_add_glacier_location(self):
        payload = json.dumps(self.addlocDict)
        response = self.wp.publish_registry("granule", self.object_uuid, payload, "PATCH")
        self.assertTrue(response)

if __name__ == '__main__':
    unittest.main()