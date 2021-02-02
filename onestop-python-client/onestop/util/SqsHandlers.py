def create_delete_handler(web_publisher):
    """
    Creates a delete function handler to be used with SqsConsumer.receive_messages.

    The delete handler queries our search api using the s3 url to retrieve a granule uuid
    and then deletes that granule from the registry.

    :param: web_publisher: WebPublisher object
    """
    def delete(records):
        if records is None:
            return
        record = records[0]
        if record['eventName'] != 'ObjectRemoved:Delete':
            return
        bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        s3_url = "s3://" + bucket + "/" + s3_key
        payload = '{"queries":[{"type": "fieldQuery", "field": "links.linkUrl", "value": "' + s3_url + '"}] }'
        search_response = web_publisher.search_onestop('granule', payload)
        response_json = search_response.json()
        if len(response_json['data']) != 0:
            granule_uuid = response_json['data'][0]['id']
            response = web_publisher.delete_registry('granule', granule_uuid)
            return response

    return delete
