from pathlib import Path, PurePath

from constructs import Construct
import aws_cdk as cdk

from .get_cdk import (
    get_external_layer, get_lambda_function, get_pythonutils_layer
)

THIS_DIRECTORY = Path(__file__).parent.absolute()
RUNTIME_DIR = str(PurePath(THIS_DIRECTORY, 'runtime'))


class LambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        utils_layer = get_pythonutils_layer(self)
        external_layer = get_external_layer(self)

        func = get_lambda_function(
            self, RUNTIME_DIR, "example-function", "runtime.handler",
            layers=[utils_layer, external_layer],
            description="Lambda extensions testing"
        )


class SecondLambdaStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        utils_layer = get_pythonutils_layer(self)
        external_layer = get_external_layer(self)

        func = get_lambda_function(
            self, RUNTIME_DIR, "second-example-function", "runtime.handler",
            layers=[utils_layer, external_layer],
            description="Lambda extensions testing"
        )
