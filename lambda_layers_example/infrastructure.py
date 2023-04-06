from pathlib import Path, PurePath

from constructs import Construct
import aws_cdk as cdk

THIS_DIRECTORY = Path(__file__).parent.absolute()
RUNTIME_DIR = str(PurePath(THIS_DIRECTORY, 'runtime'))
UTILS_DIR = str(PurePath(THIS_DIRECTORY, 'layers', 'pythonutils'))


class LambdaLayersExampleStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        layer_arn = cdk.Fn.import_value("pythonUtilsArn")
        layer = cdk.aws_lambda.LayerVersion.from_layer_version_arn(
            self, "pythonUtilsArn", layer_arn
        )

        # Create the Lambda function
        func = cdk.aws_lambda.Function(self, "example-function",
            code=cdk.aws_lambda.Code.from_asset(RUNTIME_DIR),
            handler="runtime.handler",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            layers=[layer],
            description="Lambda extensions testing"
        )


class SecondLambdaLayersExampleStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        layer_arn = cdk.Fn.import_value("pythonUtilsArn")
        layer = cdk.aws_lambda.LayerVersion.from_layer_version_arn(
            self, "pythonUtilsArn", layer_arn
        )

        # Create the Lambda function
        func = cdk.aws_lambda.Function(self, "second example-function",
            code=cdk.aws_lambda.Code.from_asset(RUNTIME_DIR),
            handler="runtime.handler",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            layers=[layer],
            description="Lambda extensions testing"
        )
