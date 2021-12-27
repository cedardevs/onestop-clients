import argparse
import yaml
import os

from onestop.util.S3Utils import S3Utils

config_dict = {}

if __name__ == '__main__':
    # Example command: python3 archive_client_integration.py -conf /Users/whoever/repo/onestop-clients/scripts/config/combined_template.yml -cred /Users/whoever/repo/onestop-clients/scripts/config/credentials.yml
    #    python3 archive_client_integration.py -cred /Users/whoever/repo/onestop-clients/scripts/config/credentials.yml
    parser = argparse.ArgumentParser(description="Launches archive client integration")
    # Set default config location to the Helm mounted pod configuration location
    parser.add_argument('-conf', dest="conf", required=False, default='/etc/config/config.yml',
                        help="AWS config filepath")
    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Generate configuration dictionary
    conf_loc = args.pop('conf')
    with open(conf_loc) as f:
        config_dict.update(yaml.load(f, Loader=yaml.FullLoader))

    # Get credentials from passed in fully qualified path or ENV.
    cred_loc = args.pop('cred')
    if cred_loc is not None:
        with open(cred_loc) as f:
            creds = yaml.load(f, Loader=yaml.FullLoader)
        registry_username = creds['registry']['username']
        registry_password = creds['registry']['password']
        access_key = creds['sandbox']['access_key']
        access_secret = creds['sandbox']['secret_key']
    else:
        print("Using env variables for config parameters")
        registry_username = os.environ.get("REGISTRY_USERNAME")
        registry_password = os.environ.get("REGISTRY_PASSWORD")
        access_key = os.environ.get("ACCESS_KEY")
        access_secret = os.environ.get("SECRET_KEY")

    config_dict.update({
        'registry_username' : registry_username,
        'registry_password' : registry_password,
        'access_key' : access_key,
        'secret_key' : access_secret
    })

    # Upload a test file to s3 bucket
    s3_utils = S3Utils(**config_dict)

    s3 = s3_utils.connect('client', 's3', config_dict['s3_region'])

    # config for s3 low level api cross origin us-west-2
    s3_cross_region = s3_utils.connect('client', 's3', config_dict['s3_region2'])
    bucket_name_cross_region = config_dict['s3_bucket2']

    overwrite = True

    # Files to upload - TODO: User should change these paths.
    local_files = ["/scripts/data/file1.csv", "/scripts/data/file2.csv"]
    for file in local_files:
        print("Uploading file: %s"%file)

        # changed the key for testing
        s3_file = "public/NESDIS/CSB/" + file
        upload = s3_utils.upload_s3(s3, file, config_dict['s3_bucket'], s3_file, overwrite)
        if not upload:
            raise Exception("Unknown, upload to s3 failed.")

        # Upload file to cross region bucket then transfer to glacier right after
        upload = s3_utils.upload_s3(s3_cross_region, file, bucket_name_cross_region, s3_file, overwrite)
        if not upload:
            raise Exception("Unknown, upload to s3 failed.")
        s3_utils.s3_to_glacier(s3_cross_region, bucket_name_cross_region, s3_file)
