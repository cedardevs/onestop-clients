import os


# This function takes a source file path and a target relative path and creates an absolute path to the target file
def abspath_from_relative(path_from, rel_path_to):
    return os.path.abspath(os.path.join(os.path.dirname(path_from), rel_path_to))


def create_delete_message(region, bucket, key):
    message = {
        "Type": "Notification",
        "MessageId": "e12f0129-0236-529c-aeed-5978d181e92a",
        "TopicArn": "arn:aws:sns:" + region + ":798276211865:cloud-archive-client-sns",
        "Subject": "Amazon S3 Notification",
        "Message": '''{
                "Records": [{
                    "eventVersion": "2.1", "eventSource": "aws:s3", "awsRegion": "''' + region + '''",
                    "eventTime": "2020-12-14T20:56:08.725Z", 
                    "eventName": "ObjectRemoved:Delete",
                    "userIdentity": {"principalId": "AX8TWPQYA8JEM"},
                    "requestParameters": {"sourceIPAddress": "65.113.158.185"},
                    "responseElements": {"x-amz-request-id": "D8059E6A1D53597A",
                                         "x-amz-id-2": "7DZF7MAaHztZqVMKlsK45Ogrto0945RzXSkMnmArxNCZ+4/jmXeUn9JM1NWOMeKK093vW8g5Cj5KMutID+4R3W1Rx3XDZOio"},
                    "s3": {
                        "s3SchemaVersion": "1.0", "configurationId": "archive-testing-demo-event",
                        "bucket": {"name": "''' + bucket + '''",
                                   "ownerIdentity": {"principalId": "AX8TWPQYA8JEM"},
                                   "arn": "arn:aws:s3:::''' + bucket + '''"},
                        "object": {"key": "''' + key + '''", "sequencer": "005FD7D1765F04D8BE"}
                    }
                }]
            }''',
        "Timestamp": "2020-12-14T20:56:23.786Z",
        "SignatureVersion": "1",
        "Signature": "MB5P0H5R5q3zOFoo05lpL4YuZ5TJy+f2c026wBWBsQ7mbNQiVxAy4VbbK0U1N3YQwOslq5ImVjMpf26t1+zY1hoHoALfvHY9wPtc8RNlYqmupCaZgtwEl3MYQz2pHIXbcma4rt2oh+vp/n+viARCToupyysEWTvw9a9k9AZRuHhTt8NKe4gpphG0s3/C1FdvrpQUvxoSGVizkaX93clU+hAFsB7V+yTlbKP+SNAqP/PaLtai6aPY9Lb8reO2ZjucOl7EgF5IhBVT43HhjBBj4JqYBNbMPcId5vMfBX8qI8ANIVlGGCIjGo1fpU0ROxSHsltuRjkmErpxUEe3YJJM3Q==",
        "SigningCertURL": "https://sns.us-east-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
        "UnsubscribeURL": "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:798276211865:cloud-archive-client-sns:461222e7-0abf-40c6-acf7-4825cef65cce"
    }
    return message
