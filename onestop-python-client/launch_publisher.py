import argparse
from onestop.KafkaPublisher import KafkaPublisher



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launches KafkaPublisher to publish kafkda topics")
    parser.add_argument('-conf', dest="conf", required=True,
                        help="Config filepath")

    args = vars(parser.parse_args())

    confLoc = args.pop('conf')

    # "discovery":
    # {
    #     "title": < granule_title_or_file_name >,
    #     "fileIdentifier": < file_id >
    # }
    # Title: Yaquina Bay, OR (P210) Bathymetric Digital Elevation Model (30 meter resolution) Derived From Source Hydrographic Survey Soundings Collected by NOAA
    # FileIdentifier: gov.noaa.ngdc.mgg.dem:yaquina_bay_p210_30m
    collection_uuid = '3ee5976e-789a-41d5-9cae-d51e7b92a247'
    content_dict = { }
    content_dict['discovery'] = {'title': 'My New Title!',
                                 'fileIdentifier': 'gov.noaa.osim.mgg.dem:yaquina_bay_p210_30m'
                                }

    print(str(content_dict))
    kafka_publisher = KafkaPublisher(confLoc)
    kafka_publisher.connect()
    kafka_publisher.publish_collection(collection_uuid, content_dict)

