import json

import boto3


class SQSHandler:
    """
    Interface for interacting with SQS.
    """

    def __init__(self):
        self.sqs = boto3.resource('sqs')

    def add_message_to_queue(self, queue_url: str, payload: dict):
        response = self.sqs.meta.client.send_message(QueueUrl=queue_url,
                                                     MessageBody=json.dumps(payload))
        status = response['ResponseMetadata']['HTTPStatusCode']
        if status != 200:
            raise Exception

    def receive_messages_from_queue(self, queue_url: str, wait_time=15, num_messages=1):
        print('sqs url', queue_url)
        response = self.sqs.meta.client.receive_message(QueueUrl=queue_url,
                                                        MaxNumberOfMessages=num_messages,
                                                        WaitTimeSeconds=wait_time)
        status = response['ResponseMetadata']['HTTPStatusCode']
        if status != 200:
            raise Exception
        return response.get('Messages')
