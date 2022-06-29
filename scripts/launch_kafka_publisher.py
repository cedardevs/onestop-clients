import argparse
import yaml

from onestop.KafkaPublisher import KafkaPublisher

if __name__ == '__main__':
    '''
    Uploads collection to Kafka collection topic 
    '''
    parser = argparse.ArgumentParser(description="Launches KafkaPublisher to publish kafka topics")
    parser.add_argument('-conf', dest="conf", required=False, default='/etc/config/config.yml',
                        help="Config filepath")

    args = vars(parser.parse_args())

    conf_loc = args.pop('conf')
    with open(conf_loc) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    # "discovery":
    # {
    #     "title": < granule_title_or_file_name >,
    #     "fileIdentifier": < file_id >
    # }
    # Title: Yaquina Bay, OR (P210) Bathymetric Digital Elevation Model (30 meter resolution) Derived From Source Hydrographic Survey Soundings Collected by NOAA
    # FileIdentifier: gov.noaa.ngdc.mgg.dem:yaquina_bay_p210_30m
    collection_uuid = '3ee5976e-789a-41d5-9cae-d51e7b92a247'
    content_dict = {'discovery': {'title': 'My Extra New Title!',
                                  'fileIdentifier': 'gov.noaa.osim2.mgg.dem:yaquina_bay_p210_30m',
                                  "links": [
                                      {
                                          "linkFunction": "download", "linkName": "Amazon S3", "linkProtocol": "HTTPS",
                                          "linkUrl": "https://s3.amazonaws.com/nesdis-incoming-data/Himawari-8/AHI-L1b-Japan/2020/05/12/1620/HS_H08_20200512_1620_B05_JP01_R20_S0101.DAT.bz2"
                                      }
                                  ]
                                  }
                    }
    # method one of POST, PUT, PATCH, DELETE
    method = 'POST' #Update

    kafka_publisher = KafkaPublisher(**conf)
    metadata_producer = kafka_publisher.connect()
    kafka_publisher.publish_collection(metadata_producer, collection_uuid, content_dict, method)

