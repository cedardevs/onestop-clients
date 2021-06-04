from onestop.util.ClientLogger import ClientLogger

def create_delete_handler(web_publisher):
    """
    Creates a delete function handler to be used with SqsConsumer.receive_messages.

    The delete handler queries our search api using the s3 url to retrieve a granule uuid
    and then deletes that granule from the registry.

    :param: web_publisher: WebPublisher object
    """
    def delete(records, log_level='INFO'):

        logger = ClientLogger.get_logger('SqsHandlers.create_delete_handler.delete', log_level, False)
        logger.info("In create_delete_handler.delete() handler")
        logger.debug("Records: %s"%records)

        if not records or records is None:
            logger.info("Ending handler, records empty, records=%s"%records)
            return

        record = records[0]
        if record['eventName'] != 'ObjectRemoved:Delete':
            logger.info("Ending handler, eventName=%s"%record['eventName'])
            return

        logger.info('Attempting to delete record %s'%record)

        bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        s3_url = "s3://" + bucket + "/" + s3_key
        payload = '{"queries":[{"type": "fieldQuery", "field": "links.linkUrl", "value": "' + s3_url + '"}] }'
        search_response = web_publisher.search_onestop('granule', payload)
        logger.debug('OneStop search response=%s'%search_response)
        response_json = search_response.json()
        logger.debug('OneStop search response json=%s'%response_json)
        logger.debug('OneStop search response data=%s'%response_json['data'])
        if len(response_json['data']) != 0:
            granule_uuid = response_json['data'][0]['id']
            response = web_publisher.delete_registry('granule', granule_uuid)
            logger.debug('web_publisher.delete_registry response: %s'%response)
            return response

        logger.warning("OneStop search response has no 'data' field. Response=%s"%response_json)

    return delete

def create_upload_handler(web_publisher, s3_utils, s3_message_adapter):
    """
    Creates a upload function handler to be used with SqsConsumer.receive_messages.

    The upload handler function checks the object for a UUID and if one is not found, it will create one for it.

    :param: web_publisher: WebPublisher object
    :param: s3_utils: S3Utils object
    :param: s3ma: S3MessageAdapter object

    """
    def upload(records, log_level='INFO'):
        logger = ClientLogger.get_logger('SqsHandlers.create_upload_handler.upload', log_level, False)
        logger.info("In create_upload_handler.upload() handler")
        logger.debug("Records: %s"%records)

        rec = records[0]
        s3_key = rec['s3']['object']['key']
        logger.info("Received message for " + s3_key)
        logger.info("Event type: " + rec['eventName'])
        bucket = rec['s3']['bucket']['name']
        logger.info("BUCKET: %s"%bucket)
        s3_resource = s3_utils.connect("s3_resource", None)

        # Fetch the object to get the uuid
        object_uuid = s3_utils.get_uuid_metadata(s3_resource, bucket, s3_key)
        if object_uuid is not None:
            logger.info("Retrieved object-uuid: %s"%object_uuid)
        else:
            logger.info("Adding uuid")
            # Can't add uuid to glacier and should be copied over
            if "backup" not in bucket:
                object_uuid = s3_utils.add_uuid_metadata(s3_resource, bucket, s3_key)

        # Convert s3 message to IM message
        json_payload = s3_message_adapter.transform(records)
        logger.debug('transformed message, json_payload: %s'%json_payload)

        # Send the message to registry
        payload = json_payload.serialize()
        method = 'PATCH' # Backup location should be patched if not backup within bucket name
        if "backup" not in bucket:
            method = 'POST'

        logger.debug('web_publisher.publish_registry method using "%s" with payload %s'%(method,payload))
        registry_response = web_publisher.publish_registry("granule", object_uuid, payload, method)
        logger.debug('web_publisher.publish_registry response=%s'%registry_response)
        logger.debug('web_publisher.publish_registry response json=%s'%registry_response.json())

        return registry_response

    return upload