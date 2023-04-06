from pathlib import Path, PurePath

from constructs import Construct
import aws_cdk as cdk

THIS_DIRECTORY = Path(__file__).parent.absolute()
RUNTIME_DIR = str(PurePath(THIS_DIRECTORY, 'runtime'))

LAYER_ARN = cdk.Fn.import_value("pythonUtilsArn")
EXTERNAL_LAYER_ARN = cdk.Fn.import_value("pythonExternalDeps")

class LambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        layer = cdk.aws_lambda.LayerVersion.from_layer_version_arn(
            self, "pythonUtilsArn", LAYER_ARN
        )
        external_layer = cdk.aws_lambda.LayerVersion.from_layer_version_arn(
            self, "pythonExternalDeps", EXTERNAL_LAYER_ARN
        )

        func = cdk.aws_lambda.Function(self, "example-function",
            code=cdk.aws_lambda.Code.from_asset(RUNTIME_DIR),
            handler="runtime.handler",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            layers=[layer, external_layer],
            description="Lambda extensions testing"
        )


class SecondLambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        layer = cdk.aws_lambda.LayerVersion.from_layer_version_arn(
            self, "pythonUtilsArn", LAYER_ARN
        )
        external_layer = cdk.aws_lambda.LayerVersion.from_layer_version_arn(
            self, "pythonExternalDeps", EXTERNAL_LAYER_ARN
        )

        func = cdk.aws_lambda.Function(self, "second example-function",
            code=cdk.aws_lambda.Code.from_asset(RUNTIME_DIR),
            handler="runtime.handler",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            layers=[layer, external_layer],
            description="Lambda extensions testing"
        )
