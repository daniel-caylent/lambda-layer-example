#!/usr/bin/env python3

import aws_cdk as cdk

from lambda_layers_example.layers.infrastructure import LambdaLayersStack
from lambda_layers_example.infrastructure import LambdaLayersExampleStack, SecondLambdaLayersExampleStack


app = cdk.App()

layers_stack = LambdaLayersStack(app, "lambda-layers-example")
lambda_stack = LambdaLayersExampleStack(app, "lambda-example")
another_lambda_stack = SecondLambdaLayersExampleStack(app, "second-lambda-layers-example")

lambda_stack.add_dependency(layers_stack)
another_lambda_stack.add_dependency(layers_stack)

app.synth()
