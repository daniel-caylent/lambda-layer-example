from pathlib import Path, PurePath

import aws_cdk as cdk


THIS_DIRECTORY = Path(__file__).parent.absolute()
LAYERS_DIR = str(PurePath(THIS_DIRECTORY.parent, 'layers'))

LAYER_ARN = cdk.Fn.import_value("pythonUtilsArn")


# CDK Factory. Separete these functions into their own module
# ('get_cdk' or something like that) for your professional apps
def get_lambda_function(context, CODE_DIR, name, handler, layers=[], description="", **kwargs):
    return cdk.aws_lambda.Function(context, name,
            code=cdk.aws_lambda.Code.from_asset(CODE_DIR),
            handler=handler,
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            layers=layers,
            description=description,
            **kwargs
        )

def get_pythonutils_layer(context):
    utils_dir = str(PurePath(LAYERS_DIR, 'pythonutils'))
    return cdk.aws_lambda.LayerVersion(context, "pythonutils-layer",
            code=cdk.aws_lambda.Code.from_asset(utils_dir),
            compatible_runtimes=[cdk.aws_lambda.Runtime.PYTHON_3_9],
            description="Lambda layer with python utils"
        )

def get_external_layer(context):
    external_layer_arn = cdk.Fn.import_value("pythonExternalDeps")
    return cdk.aws_lambda.LayerVersion.from_layer_version_arn(
        context, "external-python-layer", external_layer_arn
    )
