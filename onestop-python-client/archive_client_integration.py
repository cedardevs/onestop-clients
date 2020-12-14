import argparse
import json
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher
import logging

"""
Changes the storage class of an object from S3 to Glacier
Requires the configure and credential locations as parameters as well as the key of the object
"""
def handler_s3_to_glacier(s3_utils, key):
    print("S3 to Glacier---------")

    #grabs te region and bucket name from the config file
    region = s3_utils.conf['region']
    bucket = s3_utils.conf['s3_bucket']

    # Create boto3 low level api connection
    s3 = s3_utils.connect('s3', region)

    # Using the S3 util class invoke the change of storage class
    response = s3_utils.s3_to_glacier(s3, bucket, key)

    return response

def handler_s3_cross_region(s3_utils, key):
    print('Cross Region Vault Upload ------------- ')

    # grabs te region and bucket name from the config file
    region = s3_utils.conf['region']
    bucket = s3_utils.conf['s3_bucket']

    #makes connection to low level s3 client
    s3= s3_utils.connect('s3', region)

    # Reads object data and stores it into a variable
    file_data = s3_utils.read_bytes_s3(s3, bucket, key)

    # Redirecting upload to vault in second region
    glacier = s3_utils.connect("glacier", s3_utils.conf['region2'])
    vault_name = s3_utils.conf['vault_name2']
    print('vault name: ' + str(vault_name))
    print('region name: ' + str(s3_utils.conf['region2']))
    print('-------file data---------')
    print(file_data)
    response = s3_utils.upload_archive(glacier, vault_name, file_data)
    return response


"""
Initiates job for archive retrieval. Takes 3-5 hours to complete
"""
def handler_archive_job(s3_utils):
    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    response = s3_utils.retrieve_inventory(glacier, vault_name)
    if response is not None:
        logging.info(f'Initiated inventory-retrieval job for {vault_name}')
        logging.info(f'Retrieval Job ID: {response["jobId"]}')

    # will return jobId so we can use it to retrieve our results
    return response['jobId']

"""
Once the job has been completed, use the job id to retrieve archive results
"""
def handler_archive_results(vault_name, glacier, jobid):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Retrieve the job results
    inventory = s3_utils.retrieve_inventory_results(vault_name, glacier, jobid)
    if inventory is not None:
        # Output some of the inventory information
        logging.info(f'Vault ARN: {inventory["VaultARN"]}')
        for archive in inventory['ArchiveList']:
            logging.info(f'  Size: {archive["Size"]:6d}  '
                         f'Archive ID: {archive["ArchiveId"]}')

"""
Uses high level api to restore object from glacier to s3
"""
def handler_s3_restore(key):
    region = s3_utils.conf['region']
    bucket = s3_utils.conf['s3_bucket']

    # use high level api
    s3 = s3_utils.connect('s3_resource', region)
    s3_utils.s3_restore(s3, bucket, key)

def handler(recs):
    print("Handler...")

    # Now get boto client for object-uuid retrieval
    object_uuid = None
    bucket = None

    if recs is None:
        print( "No records retrieved" )
    else:
        rec = recs[0]
        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        print('Bucket: ' + str(bucket))
        print('s3_key: ' + str(s3_key))

        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
        if object_uuid is not None:
            print("Retrieved object-uuid: " + object_uuid)
        else:
            print("Adding uuid")
            s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

    json_payload = s3ma.transform(recs)
    print(json_payload)
    registry_response = wp.publish_registry("granule", object_uuid, json_payload, "POST")
    print(registry_response.json())


    #Upload to archive
    file_data = s3_utils.read_bytes_s3(s3, bucket, s3_key)
    glacier = s3_utils.connect("glacier", s3_utils.conf['region'])
    vault_name = s3_utils.conf['vault_name']


    resp_dict = s3_utils.upload_archive(glacier, vault_name, file_data)

    print("archiveLocation: " + resp_dict['location'])
    print("archiveId: " + resp_dict['archiveId'])
    print("sha256: " + resp_dict['checksum'])

    addlocPayload = {
        "fileLocations": {
            resp_dict['location']: {
                "uri": resp_dict['location'],
                "type": "ACCESS",
                "restricted": True,
                "locality": "us-west-2",
                "serviceType": "Amazon:AWS:Glacier",
                "asynchronous": True
            }
        }
    }
    json_payload = json.dumps(addlocPayload, indent=2)
    # Send patch request next with archive location
    registry_response = wp.publish_registry("granule", object_uuid, json_payload, "PATCH")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches archive_client_integration test")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="AWS config filepath")

    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Get configuration file path locations
    conf_loc = args.pop('conf')
    cred_loc = args.pop('cred')

    # Create instance of s3_utils
    s3_utils = S3Utils(conf_loc, cred_loc)


    # Upload a test file to s3 bucket, need to specify key
    """
    key = 'public/jeff/maroon-bells.jpg'
    handler_s3_to_glacier(s3_utils,key)
    """



    #Using glacier api initiates job and returns archive results
    """
    # Connect to your glacier vault for retrieval
    glacier = s3_utils.connect("glacier", s3_utils.conf['region2'])
    vault_name = s3_utils.conf['vault_name2']
    
    jobId= handler_archive_job(s3_utils)
    
    #after job is initiated, you need to wait 3-5 hours for handler to retrieve results
    handler_archive_results(vault_name, glacier, jobId)
    """


    # Uses s3 resource (high level api) to restore from glacier
    """
    key = 'public/jeff/maroon-bells.jpg'
    handler_s3_restore(key)
    """


    """
    # Low-level api ? Can we just use high level revisit me!
    s3 = s3_utils.connect("s3", None)

    # High-level api
    s3_resource = s3_utils.connect("s3_resource", None)

    bucket = s3_utils.conf['s3_bucket']
    overwrite = True

    sqs_max_polls = s3_utils.conf['sqs_max_polls']

    
    # Add 3 files to bucket
    local_files = ["file1.csv", "file2.csv"]
    s3_file = None
    for file in local_files:
        local_file = "tests/data/" + file
        s3_file = "csv/" + file
        s3_utils.upload_s3(s3, local_file, bucket, s3_file, overwrite)
    


    # Receive s3 message and MVM from SQS queue
    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    s3ma = S3MessageAdapter("config/csb-data-stream-config.yml")
    wp = WebPublisher("config/web-publisher-config-dev.yml", cred_loc)

    queue = sqs_consumer.connect()
    try:
        debug = False
        sqs_consumer.receive_messages(queue, sqs_max_polls, handler)

    except Exception as e:
        print("Message queue consumption failed: {}".format(e))
    """



