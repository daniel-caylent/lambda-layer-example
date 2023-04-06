import os
import time
import boto3

# this module is not found locally. It is an external dependency
# that must be provided through a lambda layer
import flask

# This library is not found locally. It is a custom module that 
# must be provided through a lambda layer
from pythonutils import utildecorator

@utildecorator
def handler(event, context):
    print("Here is the actual lambda!")

    return 'All done!'
