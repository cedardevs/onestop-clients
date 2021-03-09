import argparse
from onestop.KafkaPublisher import KafkaPublisher

if __name__ == '__main__':
    '''
    Uploads collection to Kafka collection topic 
    '''
    parser = argparse.ArgumentParser(description="Launches KafkaPublisher to publish kafkda topics")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="Config filepath")

    args = vars(parser.parse_args())

    conf_loc = args.pop('conf')

    # "discovery":
    # {
    #     "title": < granule_title_or_file_name >,
    #     "fileIdentifier": < file_id >
    # }
    # Title: Yaquina Bay, OR (P210) Bathymetric Digital Elevation Model (30 meter resolution) Derived From Source Hydrographic Survey Soundings Collected by NOAA
    # FileIdentifier: gov.noaa.ngdc.mgg.dem:yaquina_bay_p210_30m
    collection_uuid = '3ee5976e-789a-41d5-9cae-d51e7b92a247'
    content_dict = {'discovery': {'title': 'My Extra New Title!',
                                  'fileIdentifier': 'gov.noaa.osim2.mgg.dem:yaquina_bay_p210_30m'
                                  }
                    }
    # method one of POST, PUT, PATCH, DELETE
    method = 'POST' #Update

    kafka_publisher = KafkaPublisher(conf_loc)
    metadata_producer = kafka_publisher.connect()
    kafka_publisher.publish_collection(metadata_producer, collection_uuid, content_dict, method)

