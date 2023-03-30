#!/usr/bin/env python3

import aws_cdk as cdk

from lambda_ext_2.infrastructure import LambdaExt2Stack


app = cdk.App()
LambdaExt2Stack(app, "lambda-ext-2")

app.synth()
