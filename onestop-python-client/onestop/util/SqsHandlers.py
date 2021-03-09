
def create_delete_handler(web_publisher):
    """
    Creates a delete function handler to be used with SqsConsumer.receive_messages.

    The delete handler queries our search api using the s3 url to retrieve a granule uuid
    and then deletes that granule from the registry.

    :param: web_publisher: WebPublisher object
    """
    def delete(records):
        print("Delete handler handling message")
        if records is None:
            return
        record = records[0]
        if 'ObjectRemoved' not in record['eventName']:
            print("Not a delete message")
            return
        bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        s3_url = "s3://" + bucket + "/" + s3_key
        payload = '{"filters":[{"type": "field", "name": "links.linkUrl", "value": "' + s3_url + '"}] }'
        search_response = web_publisher.search_onestop('granule', payload)
        response_json = search_response.json()
        if len(response_json['data']) != 0:
            granule_uuid = response_json['data'][0]['id']
            response = web_publisher.delete_registry('granule', granule_uuid)
            return response

    return delete

#TODO make this more functional- make is so we dont pass these objects around
def create_upload_handler(web_publisher, s3_utils, s3ma):
    """
    Creates a upload function handler to be used with SqsConsumer.receive_messages.

    The upload handler function checks the object for a UUID and if one is not found, it will create one for it.

    :param: web_publisher: WebPublisher object
    :param: s3_utils: S3Utils object
    :param: s3ma: S3MessageAdapter object

    """
    def upload(records):
        print("Upload handler handling message")
        rec = records[0]
        s3_key = rec['s3']['object']['key']
        print("Received message for " + s3_key)
        print("Event type: " + rec['eventName'])
        s3_resource = s3_utils.connect("s3_resource", None)
        bucket = rec['s3']['bucket']['name']
        # Fetch the object to get the uuid
        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
        if object_uuid is not None:
            print("Retrieved object-uuid: " + object_uuid)
        else:
            print("Adding uuid")
            # Can't add uuid to glacier and should be copied over
            if "backup" not in bucket:
                object_uuid = s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

        # Convert s3 message to IM message
        json_payload = s3ma.transform(records)

        # Send the message to registry
        print("BUCKET: " + bucket + "-----")
        if "backup" not in bucket:
            registry_response = web_publisher.publish_registry("granule", object_uuid, json_payload.serialize(), "POST")
        # Backup location should be patched
        else:
            registry_response = web_publisher.publish_registry("granule", object_uuid, json_payload.serialize(), "PATCH")

        print("RESPONSE: ")
        print(registry_response.json())
        return registry_response

    return upload


#TODO this already deprecated in favor of replication at the bucket level
def create_copy_handler(web_publisher, s3_utils, s3ma, destination_bucket, destination_region):
    """
    Creates a copy function handler to be used with SqsConsumer.receive_messages.

    The copy handler function copies objects to another bucket.

    :param: web_publisher: WebPublisher object
    :param: s3_utils: S3Utils object
    :param: s3ma: S3MessageAdapter object

    """
    def copy(records):
        print("Copy handler handling message")
        rec = records[0]
        s3_key = rec['s3']['object']['key']
        print("Received message for " + s3_key)
        print("Event type: " + rec['eventName'])

        s3_resource = s3_utils.connect("s3_resource", None)
        bucket = rec['s3']['bucket']['name']

        # Fetch the object to get the uuid
        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)

        if object_uuid is not None:
            print("Retrieved object-uuid: " + object_uuid)
            copy_source = {
                'Bucket': bucket,
                'Key': s3_key
            }

            s3_resource.meta.client.copy(copy_source, destination_bucket, s3_key)
            json_payload = s3ma.transform(records, destination_bucket, "https://"+ destination_bucket + "." + destination_region + ".amazonaws.com" )
            print("COPY REQUEST: ")
            print(json_payload.serialize())
            #Send the message to Onestop
            registry_response = web_publisher.publish_registry("granule", object_uuid, json_payload.serialize(), "PATCH")
            print("RESPONSE: ")
            print(registry_response.json())
        else:
            print("No uuid")

    return copy
