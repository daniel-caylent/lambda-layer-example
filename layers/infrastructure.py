from pathlib import Path, PurePath

from constructs import Construct
import aws_cdk as cdk

THIS_DIRECTORY = Path(__file__).parent.absolute()
UTILS_DIR = str(PurePath(THIS_DIRECTORY, 'pythonutils'))
EXTERNAL_DIR = str(PurePath(THIS_DIRECTORY, 'external'))


class LambdaLayersStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        external_layer = cdk.aws_lambda.LayerVersion(self, "lambda-layer-example-external",
            code=cdk.aws_lambda.Code.from_asset(EXTERNAL_DIR),
            compatible_runtimes=[cdk.aws_lambda.Runtime.PYTHON_3_9],
            description="Lambda layer with external dependencies"
        )

        cdk.CfnOutput(
            self, "pythonExternalDeps",
            value=external_layer.layer_version_arn,
            export_name="pythonExternalDeps"
        )
