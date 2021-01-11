import json
import unittest
import boto3
import requests
import urllib.parse

from moto import mock_s3
from moto import mock_sqs
from tests.utils import abspath_from_relative
from onestop.WebPublisher import WebPublisher
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.util.SqsConsumer import SqsConsumer


class SqsDeleteTest(unittest.TestCase):
    wp = None
    su = None
    s3ma = None
    sqs = None
    wp_config = abspath_from_relative(__file__, "../config/web-publisher-config-local.yml")
    aws_config = abspath_from_relative(__file__, "../config/aws-util-config-dev.yml")
    cred_config = abspath_from_relative(__file__, "../config/credentials-template.yml")
    csb_config = abspath_from_relative(__file__, "../config/csb-data-stream-config.yml")

    object_uuid = "9f0a5ff2-fcc0-5bcb-a225-024b669c9bba"
    collection_uuid = "fdb56230-87f4-49f2-ab83-104cfd073177"
    payloadDict = {
        "fileInformation": {
            "name": "file2.csv",
            "size": 1385,
            "checksums": [{
                "algorithm": "MD5",
                "value": "44d2452e8bc2c8013e9c673086fbab7a"
            }]
        },
        "relationships": [{
            "type": "COLLECTION",
            "id": collection_uuid
        }],
        "fileLocations": {
            "archive-testing-demo/csv/file2.csv": {
                "uri": "s3://archive-testing-demo/csv/file2.csv",
                "type": "ACCESS",
                "restricted": False,
                "serviceType": "Amazon:AWS:S3",
                "asynchronous": False
            }
        },
        "discovery": {
            "title": "file2.csv",
            "parentIdentifier": collection_uuid,
            "fileIdentifier": "gov.noaa.ncei.csb:file2",
            "links": [{
                 "linkFunction": "download",
                 "linkUrl": "s3://archive-testing-demo/csv/file2.csv",
                 "linkName": "Amazon S3",
                 "linkProtocol": "Amazon:AWS:S3"
            }]
        }
    }

    s3DeleteMessage = {
        "Type": "Notification",
        "MessageId": "e12f0129-0236-529c-aeed-5978d181e92a",
        "TopicArn": "arn:aws:sns:us-east-2:798276211865:cloud-archive-client-sns",
        "Subject": "Amazon S3 Notification",
        "Message": '''{
            "Records": [{
                "eventVersion": "2.1", "eventSource": "aws:s3", "awsRegion": "us-east-2",
                "eventTime": "2020-12-14T20:56:08.725Z", "eventName": "ObjectRemoved:Delete",
                "userIdentity": {"principalId": "AX8TWPQYA8JEM"},
                "requestParameters": {"sourceIPAddress": "65.113.158.185"},
                "responseElements": {"x-amz-request-id": "D8059E6A1D53597A",
                                     "x-amz-id-2": "7DZF7MAaHztZqVMKlsK45Ogrto0945RzXSkMnmArxNCZ+4/jmXeUn9JM1NWOMeKK093vW8g5Cj5KMutID+4R3W1Rx3XDZOio"},
                "s3": {
                    "s3SchemaVersion": "1.0", "configurationId": "archive-testing-demo-event",
                    "bucket": {"name": "archive-testing-demo",
                               "ownerIdentity": {"principalId": "AX8TWPQYA8JEM"},
                               "arn": "arn:aws:s3:::archive-testing-demo"},
                    "object": {"key": "csv/file2.csv", "sequencer": "005FD7D1765F04D8BE"}
                }
            }]
        }''',
        "Timestamp": "2020-12-14T20:56:23.786Z",
        "SignatureVersion": "1",
        "Signature": "MB5P0H5R5q3zOFoo05lpL4YuZ5TJy+f2c026wBWBsQ7mbNQiVxAy4VbbK0U1N3YQwOslq5ImVjMpf26t1+zY1hoHoALfvHY9wPtc8RNlYqmupCaZgtwEl3MYQz2pHIXbcma4rt2oh+vp/n+viARCToupyysEWTvw9a9k9AZRuHhTt8NKe4gpphG0s3/C1FdvrpQUvxoSGVizkaX93clU+hAFsB7V+yTlbKP+SNAqP/PaLtai6aPY9Lb8reO2ZjucOl7EgF5IhBVT43HhjBBj4JqYBNbMPcId5vMfBX8qI8ANIVlGGCIjGo1fpU0ROxSHsltuRjkmErpxUEe3YJJM3Q==",
        "SigningCertURL": "https://sns.us-east-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
        "UnsubscribeURL": "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:798276211865:cloud-archive-client-sns:461222e7-0abf-40c6-acf7-4825cef65cce"
    }

    def setUp(self):
        print("Set it up!")
        self.wp = WebPublisher(self.wp_config, self.cred_config)
        self.su = S3Utils(self.aws_config, self.cred_config)
        self.s3ma = S3MessageAdapter(self.csb_config)
        self.publish(self.payloadDict)

    def tearDown(self):
        print("Tear it down!")
        self.delete()

    @mock_s3
    @mock_sqs
    def init_s3(self):
        boto_client = self.su.connect("s3", None)
        file = "file2.csv"
        bucket = self.su.conf['s3_bucket']
        boto_client.create_bucket(Bucket=bucket)
        s3_key = "csv/" + file
        boto_client.put_object(Bucket=bucket, Key=s3_key, Body="foobar")

        sqs_client = boto3.client('sqs', region_name=self.su.conf['s3_region'])
        sqs_queue = sqs_client.create_queue(QueueName="test_queue")
        self.su.conf['sqs_url'] = sqs_queue['QueueUrl']
        self.sqs = SqsConsumer(self.aws_config, self.cred_config)
        sqs_client.send_message(QueueUrl=self.su.conf['sqs_url'], MessageBody=json.dumps(self.s3DeleteMessage))

    def publish(self, payload_dict):
        payload = json.dumps(payload_dict)
        self.wp.publish_registry("granule", self.object_uuid, payload, "POST")

    def delete(self):
        self.wp.delete_registry("granule", self.object_uuid)

    def delete_handler(self, records):
        if records is None:
            print("No records retrieved")
            return
        rec = records[0]
        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        s3_url = "s3://" + bucket + "/" + s3_key
        payload = '{"queries":[{"type": "fieldQuery", "field": "links.linkUrl", "value": "' + s3_url + '"}],"filters":[{"type":"collection","values":["' + self.collection_uuid + '"]} ]}'
        headers = {'Content-Type': 'application/json'}
        onestop_url = self.wp.conf['onestop_base_url'] + "/granule"

        print("Get: " + onestop_url)
        response = requests.get(url=onestop_url, headers=headers, data=payload, verify=False)
        self.assertTrue(response)

    @mock_sqs
    def test_delete_handler(self):
        self.init_s3()
        sqs_queue = boto3.resource('sqs', region_name=self.su.conf['s3_region']).Queue(self.su.conf['sqs_url'])
        self.sqs.receive_messages(sqs_queue, 2, self.delete_handler)
