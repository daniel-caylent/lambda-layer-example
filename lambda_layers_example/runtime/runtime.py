import os
import time
import boto3

from pythonutils import killswitch

@killswitch
def handler(event, context):
    for record in event['Records']:
        print('Inside the lambda, doing normal stuff!!')

    return 'All done!'
