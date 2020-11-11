import yaml
import json
import unittest

from onestop.WebPublisher import WebPublisher

class WebPublisherTest(unittest.TestCase):
    wp = None
    object_uuid = "9f0a5ff2-fcc0-5bcb-a225-024b669c9bba"
    payloadDict = {
        "file_information": [
            {"name": "file2.csv"},
            {"size": 1385},
            {"checksums": [
                    {"algorithm": "MD5"},
                    { "value": "44d2452e8bc2c8013e9c673086fbab7a"}
                ]
            }
        ],
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

    def setUp(self):
        print("Set it up!")
        self.wp = WebPublisher("../config/web-publisher-config-dev.yml", "../config/credentials.yml")

    def tearDown(self):
        print("Tear it down!")

    def test_parse_config(self):
        self.assertFalse(self.wp.conf['url']==None)
        self.assertFalse(self.wp.cred['registry']['username'] == None)

    def test_publish(self):
        payload = json.dumps(self.payloadDict)
        response = self.wp.publish("granule", self.object_uuid, payload)
        print (response.json())


if __name__ == '__main__':
    unittest.main()