import argparse
from onestop.util.S3Utils import S3Utils


def handler():
    '''
    Simultaneously upload files to main bucket 'noaa-nccf-dev' in us-east-2 and glacier in cross region bucket 'noaa-nccf-dev-archive' in us-west-2.

    :return: str
        Returns response from boto3 indicating if upload was successful.
    '''
    print("Handler...")

    # config for s3 low level api for us-east-2
    s3 = s3_utils.connect('s3', s3_utils.conf['s3_region'])
    bucket_name = s3_utils.conf['s3_bucket']

    # config for s3 low level api cross origin us-west-2
    s3_cross_region = s3_utils.connect('s3', s3_utils.conf['s3_region2'])
    bucket_name_cross_region = s3_utils.conf['s3_bucket2']

    overwrite = True

    # Add 3 files to bucket
    local_files = ["file1.csv", "file2.csv"]
    s3_file = None
    for file in local_files:
        local_file = "tests/data/" + file
        # changed the key for testing
        s3_file = "public/NESDIS/CSB/" + file
        s3_utils.upload_s3(s3, local_file, bucket_name, s3_file, overwrite)

        # Upload file to cross region bucket then transfer to glacier right after
        s3_utils.upload_s3(s3_cross_region, local_file, bucket_name_cross_region, s3_file, overwrite)
        s3_utils.s3_to_glacier(s3_cross_region, bucket_name_cross_region, s3_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches archive client integration")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="AWS config filepath")

    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Get configuration file path locations
    conf_loc = args.pop('conf')
    cred_loc = args.pop('cred')

    # Upload a test file to s3 bucket
    s3_utils = S3Utils(conf_loc, cred_loc)

    handler()





        





