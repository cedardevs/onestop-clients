import yaml
import argparse
from onestop.KafkaConsumer import KafkaConsumer
from onestop.util.ClientLogger import ClientLogger

config_dict = {}

def handler(key, value, log_level = 'INFO'):
    '''
    Prints key, value pair of items in topic

    :param key: str
        kafka key
    :param value: dict
        information from item associated with the key

    :return: None
    '''
    logger = ClientLogger.get_logger('smeFunc.handler', log_level, False)
    logger.info('In Handler')
    logger.info('key=%s value=%s'%(key, value))

    """
    if (value['type'] == 'collection' or not bool(value['fileInformation'])):
        print(value['discovery']['fileIdentifier'])
    else:
        print(value['fileInformation']['name'])
    """


if __name__ == '__main__':
    # Example command: python3 smeFunc.py -conf /Users/whoever/repo/onestop-clients/scripts/config/combined_template.yml
    #    python3 smeFunc.py
    parser = argparse.ArgumentParser(description="Launches smeFunc test")
    # Set default config location to the Helm mounted pod configuration location
    parser.add_argument('-conf', dest="conf", required=False, default='/etc/config/config.yml',
                        help="AWS config filepath")
    args = vars(parser.parse_args())

    # Generate configuration dictionary
    conf_loc = args.pop('conf')
    with open(conf_loc) as f:
        config_dict.update(yaml.load(f, Loader=yaml.FullLoader))

    kafka_consumer = KafkaConsumer(**config_dict)
    kafka_consumer.granule_topic_consume = 'psi-granule-parsed'
    metadata_consumer = kafka_consumer.connect()
    kafka_consumer.consume(metadata_consumer, handler)
