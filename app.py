#!/usr/bin/env python3

import aws_cdk as cdk

from lambda_layers_example.layers.infrastructure import LambdaLayersStack
from lambda_layers_example.infrastructure import LambdaLayersExampleStack, SecondLambdaLayersExampleStack


app = cdk.App()

LambdaLayersStack(app, "lambda-layers-example")
LambdaLayersExampleStack(app, "lambda-example")
SecondLambdaLayersExampleStack(app, "second-lambda-layers-example")
app.synth()
