from onestop.util.ClientLogger import ClientLogger

def create_delete_handler(web_publisher):
    """
    Creates a delete function handler to be used with SqsConsumer.receive_messages.

    The delete handler queries our search api using the s3 url to retrieve a granule uuid
    and then deletes that granule from the registry.

    :param: web_publisher: WebPublisher object
    """
    def delete(records, log_level='INFO'):

        logger = ClientLogger.get_logger('SqsHandlers', log_level, False)
        logger.info("In create_delete_handler.delete() handler")
        logger.debug("Records: %s"%records)

        if not records or records is None:
            logger.info("Ending handler, records empty, records=%s"%records)
            return

        record = records[0]
        if record['eventName'] != 'ObjectRemoved:Delete':
            logger.info("Ending handler, eventName=%s"%record['eventName'])
            return

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
            print('delete_registry response: %s'%response)
            return response

        logger.warning("OneStop search response has no 'data' field. Response=%s"%response_json)

    return delete
