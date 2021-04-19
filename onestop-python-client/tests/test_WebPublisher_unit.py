import json
import unittest

from unittest.mock import ANY
from unittest import mock
from moto import mock_s3
from onestop.WebPublisher import WebPublisher

class WebPublisherTest(unittest.TestCase):
    username="admin"
    password="a_password"
    uuid = "9f0a5ff2-fcc0-5bcb-a225-024b669c9bba"
    registry_base_url = "https://localhost/onestop/api/registry"
    registry_full_url_granule = registry_base_url + "/metadata/granule/" + uuid
    registry_full_url_collection = registry_base_url + "/metadata/collection/" + uuid
    onestop_base_url = "https://localhost/onestop/api/search"

    payloadDict = {
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


    def setUp(self):
        print("Set it up!")

        self.wp = WebPublisher(self.registry_base_url,
                               self.username,
                               self.password,
                               self.onestop_base_url,
                               'DEBUG')

    def tearDown(self):
        print("Tear it down!")

    def mocked_requests_patch(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        print ("args: "+str(args)+" kwargs: "+str(kwargs))

        return MockResponse({"key1":"value1"}, 200)

    @mock_s3
    @mock.patch('requests.post', side_effect=mocked_requests_patch, autospec=True)
    def test_publish(self, mock_get):
        payload = json.dumps(self.payloadDict)
        self.wp.publish_registry("granule", self.uuid, payload, "POST")

        mock_get.assert_called_with(url = self.registry_full_url_granule, auth = ANY, data = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = (self.username, self.password), data = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = payload, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = ANY, verify = False, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = ANY, verify = ANY, headers = {'Content-Type': 'application/json'})

    @mock_s3
    @mock.patch('requests.put', side_effect=mocked_requests_patch, autospec=True)
    def test_publish(self, mock_get):
        payload = json.dumps(self.payloadDict)
        self.wp.publish_registry("granule", self.uuid, payload, "PUT")

        mock_get.assert_called_with(url = self.registry_full_url_granule, auth = ANY, data = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = (self.username, self.password), data = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = payload, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = ANY, verify = False, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = ANY, verify = ANY, headers = {'Content-Type': 'application/json'})

    @mock_s3
    @mock.patch('requests.patch', side_effect=mocked_requests_patch, autospec=True)
    def test_add_glacier_location(self, mock_get):
        payload = json.dumps(self.addlocDict)
        self.wp.publish_registry("granule", self.uuid, payload, "PATCH")

        mock_get.assert_called_with(url = self.registry_full_url_granule, auth = ANY, data = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = (self.username, self.password), data = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = payload, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = ANY, verify = False, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, data = ANY, verify = ANY, headers = {'Content-Type': 'application/json'})

    @mock_s3
    @mock.patch('requests.delete', side_effect=mocked_requests_patch, autospec=True)
    def test_delete_registry_granule(self, mock_get):
        self.wp.delete_registry("granule", self.uuid)

        mock_get.assert_called_with(url = self.registry_full_url_granule, headers = ANY, auth = ANY, verify = ANY)
        mock_get.assert_called_with(url = ANY, auth = (self.username, self.password), verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, verify = False, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, verify = ANY, headers = {'Content-Type': 'application/json'})

    @mock_s3
    @mock.patch('requests.delete', side_effect=mocked_requests_patch, autospec=True)
    def test_delete_registry_collection(self, mock_get):
        self.wp.delete_registry("collection", self.uuid)

        mock_get.assert_called_with(url = self.registry_full_url_collection, headers = ANY, auth = ANY, verify = ANY)
        mock_get.assert_called_with(url = ANY, auth = (self.username, self.password), verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, verify = ANY, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, verify = False, headers = ANY)
        mock_get.assert_called_with(url = ANY, auth = ANY, verify = ANY, headers = {'Content-Type': 'application/json'})

if __name__ == '__main__':
    unittest.main()