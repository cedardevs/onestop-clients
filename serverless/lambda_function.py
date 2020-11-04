import json
import requests

import conf
from ImMessage import ImMessage
from FileMessage import FileMessage
from Link import Link


def lambda_handler(event, context):
    registry_url = conf.PSI_REGISTRY_URL + "/metadata/granule"

    for rec in event['Records']:

        body = rec['body']

        msg = json.loads(body)

        #print(msg)
        # msg = json.loads(msg_json['Message'])
        recs = msg['Records']

        rec = recs[0]  # This is standard format 1 record per message for now according to AWS docs

        evt_name = rec['eventName']
        evt_time = rec['eventTime']
        prc_id = rec['userIdentity']['principalId']

        print(evt_name)
        # Mostly interested in uploads for now
        if (evt_name == "ObjectCreated:Put" or evt_name == "ObjectCreated:CompleteMultipartUpload"):
            im_message = ImMessage()
            pos = rec['s3']['object']['key'].rfind('/') + 1

            im_message.alg['algorithm'] = "MD5"
            # REVIEWME what to do if multipart upload
            im_message.alg_value['value'] = rec['s3']['object']['eTag']

            file_name = str(rec['s3']['object']['key'])[pos:]
            im_message.file_name['name'] = file_name
            im_message.file_size['size'] = rec['s3']['object']['size']
            im_message.file_format['format'] = conf.FORMAT
            im_message.headers['headers'] = conf.HEADERS

            relationship = {}
            relationship['type'] = str(conf.TYPE)
            relationship['id'] = str(conf.COLLECTION_ID)
            im_message.append_relationship(relationship)

            s3_obj_uri = "s3://" + rec['s3']['bucket']['name'] + "/" + rec['s3']['object']['key']
            file_message = FileMessage(s3_obj_uri, "ARCHIVE", True, "Amazon:AWS:S3", False)

            im_message.set_file_locations(file_message)

            access_obj_uri = conf.ACCESS_BUCKET + "/" + rec['s3']['object']['key']
            file_message = FileMessage(access_obj_uri, "ACCESS", False, "HTTPS", False)
            # file_message.fl_lastMod['lastModified'] = TBD ISO conversion to millis

            im_message.set_file_locations(file_message)

            # Discovery block
            im_message.discovery['title'] = file_name
            im_message.discovery['parentIdentifier'] = conf.COLLECTION_ID
            im_message.discovery['fileIdentifier'] = "gov.noaa.ncei.csb:" + file_name[:-4]

            link = Link("download", "Amazon S3", "HTTPS", access_obj_uri)
            im_message.append_link_attributes(link)

            link = Link("download", "Amazon S3", "Amazon:AWS:S3", s3_obj_uri)
            im_message.append_link_attributes(link)

            payload = im_message.serialize()

            # Log payload
            print(payload)

            headers = {'Content-Type': 'application/json'}

            print("Posting to: " + registry_url)
            r = requests.post(url=registry_url, headers=headers, data=payload, verify=False)
            print(r.json())

            print("lambda execution finished with post")