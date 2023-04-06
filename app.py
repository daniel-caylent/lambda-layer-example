#!/usr/bin/env python3

import aws_cdk as cdk

from layers.infrastructure import LambdaLayersStack
from lambdamodule.infrastructure import LambdaStack, SecondLambdaStack


app = cdk.App()

layers_stack = LambdaLayersStack(app, "lambda-layers-example")
lambda_stack = LambdaStack(app, "lambda-example")
another_lambda_stack = SecondLambdaStack(app, "second-lambda-example")

lambda_stack.add_dependency(layers_stack)
another_lambda_stack.add_dependency(layers_stack)

app.synth()
