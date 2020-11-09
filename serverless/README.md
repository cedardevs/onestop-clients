### Overview
lambda_function.py expects to receive an s3 message triggered from an sqs queue

The s3 message is mapped to Inventory Managers format and a post is the made to the psi registry.

There is a configuration file

### Assumption
Current implementation assumes a one-to-one mapping of SNS -> SQS -> LAMBDA -> PSI-REGISTRY per collection.

#### Manual Integration Testing Notes
- Upload CSB Collection from onestop-test-data to OSIM
- Use CSB collection fdb56230-87f4-49f2-ab83-104cfd073177
- Make sure SQS trigger is enabled for the lambda
- Ensure lambda has access to the VPC running OSIM (or use basic auth) to publish to registry
- onestop-clients has an S3Upload test you can use to upload files to s3
- Delete curl -k --user user1:mypwd -X DELETE https://ab76afcf90ee844ea95ba43a75c3624c-1204932138.us-east-1.elb.amazonaws.com/registry/metadata/granule/$uuid

#### Access Policy