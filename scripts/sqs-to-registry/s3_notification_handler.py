import os
from onestop.util.SqsConsumer import SqsConsumer
from onestop.util.S3Utils import S3Utils
from onestop.util.S3MessageAdapter import S3MessageAdapter
from onestop.WebPublisher import WebPublisher


def handler(recs):
    print("Handling message...")

    # Now get boto client for object-uuid retrieval
    object_uuid = None

    if recs is None:
        print("No records retrieved")
    else:
        rec = recs[0]
        bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']

        s3_resource = s3_utils.connect("s3_resource", None)
        print(s3_resource)
        # Fetch the object to get the uuid
        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)

        if object_uuid is not None:
            print("Retrieved object-uuid: " + object_uuid)
        else:
            print("Adding uuid")
            object_uuid = s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

    # Convert s3 message to IM message
    s3ma = S3MessageAdapter(conf_loc, s3_utils)
    json_payload = s3ma.transform(recs)

    #Send the message to Onestop
    wp = WebPublisher(conf_loc, cred_loc)
    registry_response = wp.publish_registry("granule", object_uuid, json_payload.serialize(), "POST")
    print("RESPONSE: ")
    print(registry_response.json())

if __name__ == '__main__':

    #This is where helm will mount the config
    conf_loc = "/etc/config/config.yml"
    #this is where we are about to write the cred yaml
    cred_loc = "creds.yml"

    registry_user = os.environ.get("REGISTRY_USERNAME")
    registry_pwd = os.environ.get("REGISTRY_PASSWORD")
    access_key = os.environ.get("ACCESS_KEY")
    access_secret = os.environ.get("SECRET_KEY")

    f = open(cred_loc, "w+")

#TODO revisit this when we make a standard that all scripts will follow
    #write creds to a file to avoid changing the python library
    s = """sandbox:
  access_key: {key}
  secret_key: {secret}

registry:
  username: {user}
  password: {pw}
    """.format(key=access_key, secret=access_secret, user=registry_user, pw=registry_pwd)
    f.write(s)
    f.close()
    r = open(cred_loc, "r")

    # # Receive s3 message and MVM from SQS queue
    s3_utils = S3Utils(conf_loc, cred_loc)
    sqs_max_polls = s3_utils.conf['sqs_max_polls']
    sqs_consumer = SqsConsumer(conf_loc, cred_loc)
    queue = sqs_consumer.connect()

    try:
        debug = False
        # # Pass in the handler method
        #Hack to make this stay up forever
        #TODO add feature to client library for polling indefinitely
        while True:
            sqs_consumer.receive_messages(queue, sqs_max_polls, handler)

    except Exception as e:
        print("Message queue consumption failed: {}".format(e))
