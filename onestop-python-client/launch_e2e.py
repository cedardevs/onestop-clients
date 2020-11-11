import argparse
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches e2e test")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="AWS config filepath")

    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    conf_loc = args.pop('conf')
    cred_loc = args.pop('cred')

    s3_utils = S3Utils(conf_loc, cred_loc)
    s3 = s3_utils.connect("s3", None)
    local_file = "tests/data/file1.csv"
    s3_file = "csv/file1.csv"
    bucket = s3_utils.conf['s3_bucket']
    overwrite = True

    s3_utils.upload_s3(s3, local_file, bucket, s3_file, overwrite)

    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    s3ma = S3MessageAdapter("config/csb-data-stream-config.yml")
    wp = WebPublisher("config/web-publisher-config-dev.yml", cred_loc)

    queue = sqs_consumer.connect()

    #Use call back here?
    debug = False
    recs = sqs_consumer.receive_messages(queue)
    print(recs)

    # Now get boto client for object-uuid retrieval
    object_uuid = None

    if recs is None:
        print("No records retrieved")
    else:
        rec = recs[0]
        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']

        object_uuid = s3_utils.get_uuid_metadata(s3, bucket, s3_key)
        print("Retrieved object-uuid: " + object_uuid)

    payload = s3ma.transform(recs)
    print(payload)
    registry_response = wp.publish_registry("granule", object_uuid, payload)
    print(registry_response.json())

    #Upload to archive
    file_data = s3_utils.read_bytes_s3(s3, bucket, s3_key)
    glacier = s3_utils.connect("glacier", s3_utils.conf['region'])
    vault_name = s3_utils.conf['vault_name']
    bucket = s3_utils.conf['s3_bucket']
    resp_dict = s3_utils.upload_archive(glacier, vault_name, file_data)

    # print(str(resp_dict))
    print("archiveLocation: " + resp_dict['location'])
    print("archiveId: " + resp_dict['archiveId'])
    print("sha256: " + resp_dict['checksum'])


