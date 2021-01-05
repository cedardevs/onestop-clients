import argparse
import json
from onestop.util.S3Utils import S3Utils


def handler():
    print("Bucket Automation")
    # connect to low level api
    s3 = s3_utils.connect("s3", s3_utils.conf['region'])

    # Create bucket name
    bucket_name = "noaa-nccf-dev"


    """
    - Create bucket
    - need to specify bucket location for every region except us-east-1 -> https://github.com/aws/aws-cli/issues/2603
    """
    s3.create_bucket(Bucket= bucket_name,CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2',
    },)


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
    bucket_policy = json.dumps(bucket_policy)

    #Set new bucket policy
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

    # response = s3.put_bucket_acl(
    #     #     ACL='public-read',
    #     #     AccessControlPolicy={
    #     #         'Grants': [
    #     #             {
    #     #                 'Grantee': {
    #     #                     'DisplayName': 'string',
    #     #                     'EmailAddress': 'string',
    #     #                     'ID': 'string',
    #     #                     'Type': 'CanonicalUser'|'AmazonCustomerByEmail'|'Group',
    #     #                     'URI': 'string'
    #     #                 },
    #     #                 'Permission': 'FULL_CONTROL'|'WRITE'|'WRITE_ACP'|'READ'|'READ_ACP'
    #     #             },
    #     #         ],
    #     #         'Owner': {
    #     #             'DisplayName': 'string',
    #     #             'ID': 'string'
    #     #         }
    #     #     },
    #     #     Bucket=bucket_name,
    #     #     GrantFullControl='string',
    #     #     GrantRead='string',
    #     #     GrantReadACP='string',
    #     #     GrantWrite='string',
    #     #     GrantWriteACP='string',
    #     #     ExpectedBucketOwner='string'
    #     # )


    """
    - Set ACL for public read
    """
    s3.put_bucket_acl(
        ACL='public-read',
        Bucket=bucket_name
    )

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