from functools import wraps
import os

import boto3

def killswitch(func):
    """
    Use as a decorator to switch a service off if it's malfunctioning
    To switch off, set an environment variable:
    
    KILL = 1
    """
    @wraps(func)
    def wrapper(event, context):
        kill = int(os.environ.get('KILL', 0))
        if kill:
            print('Killed!!')
            
            # send event back to queue
            resubmit_event(event)
            return
        
        print('doing normal lambda stuff')
        result = func(event, context)

        return result
    return wrapper

def resubmit_event(event):
    """
    Resubmits individual records in a Lambda event
    to the SQS queue which triggered the lambda run
    """
    print(f"Resubmitting event to SQS: {event}")

    for record in event['Records']:
        queue_name = record['eventSourceARN'].split(":")[-1]
        client = boto3.client('sqs')
        url = client.get_queue_url(QueueName=queue_name)['QueueUrl']

        print(f"Queue Name: {queue_name}\nQueue Url: {url}")
        response = client.send_message(QueueUrl=url, MessageBody=record['body'], DelaySeconds=900)

        return response
  