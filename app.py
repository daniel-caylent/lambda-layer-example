#!/usr/bin/env python3

import aws_cdk as cdk

from lambda_layers_example.infrastructure import LambdaLayersExampleStack


app = cdk.App()
LambdaLayersExampleStack(app, "lambda-layers-example")

app.synth()
