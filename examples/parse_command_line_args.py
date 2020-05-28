from argparse import ArgumentParser


def kafka_command_line_args():
    arg_parser = ArgumentParser(description='add kafka related values ... ')

    arg_parser.add_argument('--topic', required=True, help='Topic name')
    arg_parser.add_argument('--bootstrap-servers', required=False, default='localhost:9092', help='Bootstrap server address')
    arg_parser.add_argument('--schema-registry', required=False, default='http://localhost:8081', help='Schema Registry url')
    arg_parser.add_argument('--schema-file', required=False, help='File name of Avro schema to use')
    arg_parser.add_argument('--record-key', required=False, type=str, help='Record key. If not provided, will be a random UUID')
    arg_parser.add_argument('--record-value', required=False, help='Record value')

    return arg_parser.parse_args()


def sqs_command_line_args():
    arg_parser = ArgumentParser(description='add sqs related values ... ')

    arg_parser.add_argument('--node-role-name', required=True, help='role name')
    arg_parser.add_argument('--sqs-queue-url', required=True, default='', help='sqs url')
    arg_parser.add_argument('--bootstrap-servers', required=True, default='localhost:9092', help='Bootstrap server address')
    arg_parser.add_argument('--schema-registry', required=True, default='http://localhost:8081', help='Schema Registry url')
    arg_parser.add_argument('--topic-name', required=True, default='psi-granule-input-unknown', help='Topic name')

    values = arg_parser.parse_args()

    return values

