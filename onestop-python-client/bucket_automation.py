import argparse
import json
from onestop.util.S3Utils import S3Utils


def handler():
    print("Bucket Automation")
    # connect to low level api
    s3 = s3_utils.connect("s3", s3_utils.conf['s3_region'])

    # use s3_resource api to check if the bucket exists
    s3_resource = s3_utils.connect("s3_resource", s3_utils.conf['s3_region'])

    # Create bucket name
    bucket_name = "noaa-nccf-dev"

    # checks to see if the bucket is already created, if it isn't create yet then it will create the bucket, set bucket policy, and create key paths
    if not s3_resource.Bucket(bucket_name) in s3_resource.buckets.all():
        """
            - Create bucket
            - need to specify bucket location for every region except us-east-1 -> https://github.com/aws/aws-cli/issues/2603
            """
        s3.create_bucket(Bucket=bucket_name,
                         CreateBucketConfiguration={'LocationConstraint': s3_utils.conf['s3_region']},
                         ObjectLockEnabledForBucket=True)

        # Create bucket policy
        bucket_policy = {
            "Version": "2012-10-17",
            "Id": "Policy1605737714816",
            "Statement": [
                {
                    "Sid": "Stmt1605737712384",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f'arn:aws:s3:::{bucket_name}/public/*'
                }]
        }

        # Convert the policy from JSON dict to string
        bucket_policy = json.dumps(bucket_policy)

        # Set new bucket policy
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches e2e test")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="AWS config filepath")

    parser.add_argument('-cred', dest="cred", required=True,
                        help="Credentials filepath")
    args = vars(parser.parse_args())

    # Get configuration file path locations
    conf_loc = args.pop('conf')
    cred_loc = args.pop('cred')

    # Create S3Utils instance
    s3_utils = S3Utils(conf_loc, cred_loc)

    handler()