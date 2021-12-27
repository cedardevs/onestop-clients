import argparse
import json
import os
import yaml

from onestop.util.S3Utils import S3Utils

config_dict = {}

def handler():
    '''
    Creates bucket with defined key paths

    :return: str
        Returns boto3 response indicating if bucket creation was successful
    '''
    # connect to low level api
    s3 = s3_utils.connect('client', 's3', config_dict['s3_region'])

    # use s3_resource api to check if the bucket exists
    s3_resource = s3_utils.connect('resource', 's3', config_dict['s3_region'])

    # Create bucket name
    bucket_name = "noaa-nccf-dev"

    # Create bucket policy
    bucket_policy = {
        "Version": "2012-10-17",
        "Id": "noaa-nccf-dev-policy",
        "Statement": [
            {
                "Sid": "PublicRead",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f'arn:aws:s3:::{bucket_name}/public/*'
            }]
    }
    # Convert the policy from JSON dict to string
    bucket_policy_str = json.dumps(bucket_policy)

    # checks to see if the bucket is already created, if it isn't create it, then it will create the bucket, set bucket policy, and create key paths
    if not s3_resource.Bucket(bucket_name) in s3_resource.buckets.all():
        """
        - Create bucket
        - need to specify bucket location for every region except us-east-1 -> https://github.com/aws/aws-cli/issues/2603
        """
        s3.create_bucket(Bucket=bucket_name,
                         CreateBucketConfiguration={'LocationConstraint': config_dict['s3_region']},
                         ObjectLockEnabledForBucket=True)

        # Set new bucket policy
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_str)

        """
        - Create Public Key Paths
        - Have to supply Body parameter in order to create directory
        """
        s3.put_object(Bucket=bucket_name, Body='', Key='public/')

        # NESDIS key path and its sub directories
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NESDIS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NESDIS/CSB/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NESDIS/GOES/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NESDIS/H8/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NESDIS/URMA/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NESDIS/Review/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NESDIS/SAB/')

        s3.put_object(Bucket=bucket_name, Body='', Key='public/NMFS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NOS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/NWS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/OMAO/')
        s3.put_object(Bucket=bucket_name, Body='', Key='public/OAR/')

        # Create Public Key Paths
        s3.put_object(Bucket=bucket_name, Body='', Key='private/')
        # NESDIS key path and its sub directories
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NESDIS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NESDIS/CSB/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NESDIS/GOES/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NESDIS/H8/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NESDIS/URMA/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NESDIS/Review/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NESDIS/SAB/')

        s3.put_object(Bucket=bucket_name, Body='', Key='private/NMFS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NOS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/NWS/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/OMAO/')
        s3.put_object(Bucket=bucket_name, Body='', Key='private/OAR/')

    else:
        #Set bucket policy
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_str)

    # Set CORS bucket config
    cors_config = {
        'CORSRules' : [
            {
                "AllowedHeaders": [
                    "*"
                ],
                "AllowedMethods": [
                    "PUT",
                    "POST",
                    "DELETE",
                    "GET"
                ],
                "AllowedOrigins": [
                    "*"
                ],
                "ExposeHeaders": []
            }
        ]
    }
    s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_config)

    """
    - Set ACL for public read
    """
    s3.put_public_access_block(
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        },
        Bucket=bucket_name
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches e2e test")
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

    # Create S3Utils instance
    s3_utils = S3Utils(**config_dict)

    handler()