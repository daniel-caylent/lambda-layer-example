from pathlib import Path, PurePath

from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as event_sources
)

THIS_DIRECTORY = Path(__file__).parent.absolute()
RUNTIME_DIR = str(PurePath(THIS_DIRECTORY, 'runtime'))
UTILS_DIR = str(PurePath(THIS_DIRECTORY, 'layers', 'pythonutils'))


class LambdaExt2Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the Lambda layer
        layer = _lambda.LayerVersion(self, "lambda-extension-test-python-utils",
            code=_lambda.Code.from_asset(UTILS_DIR),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="Lambda extension test python utils"
        )

        queue = sqs.Queue(
            self, "extension-test-queue",
            visibility_timeout=Duration.seconds(10),
        )

        # Create the Lambda function
        func = _lambda.Function(self, "lambda-extension-test",
            code=_lambda.Code.from_asset(RUNTIME_DIR),
            handler="runtime.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[layer],
            description="Lambda extensions testing"
        )

        queuePolicy = iam.PolicyStatement(
            resources=[queue.queue_arn],
            actions=["*"]
        )

        func.add_to_role_policy(queuePolicy)

        func.add_event_source(
            event_sources.SqsEventSource(queue)
        )

