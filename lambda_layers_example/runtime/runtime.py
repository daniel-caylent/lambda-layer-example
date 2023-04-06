import os
import time
import boto3

# This library is not found locally. It must be provided through a
# lambda layer
from pythonutils import utildecorator

@utildecorator
def handler(event, context):
    print("Here is the actual lambda!")

    return 'All done!'
