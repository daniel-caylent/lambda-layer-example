Project that implements a two simple lambda functions and a lambda layer shared by both. There are some gotchas involved that can make using lambda layers confusing and I'm going to attempt to help you sidestep some of them. The main issues I had when implementing this the first time were:

1. How can you get AWS to properly provide the code in your layer to your functions
2. How can you attach a single lambda layer to lambda functions located in different stacks without duplicating code or generating additional layers or layer versions

# Directory structure
AWS Lambda layers use a very specific directory structure. In order to solve #1 above your customer lambda layers must mirror the following structure:

    -project-dir
      -layers
        -my_layer         <-- This is the entry point for the lambda layer
          requirements.txt
          -python         <-- this directory MUST be named "python"
            my_layer.py   <-- custom layer
            flask         <-- all modules must be available at the top level
            sqlachemy         of the python directory
        -another-layer    <-- a second more complex customer layer
          -python
            -another_layer
              __init__.py
              module1.py
              module2.py
      -my_application
        my_app_infrastructure.py
        my_app_runtime.py
      app.py

Adding external libraries to your layer is easy, but requires an extra build step before deployment. During the build step, any dependencies for the lambda layer need to be downloaded and included within the `python` directory. Since we include a `requirements.txt`, this can be achieved from inside the `project-dir` by running:

    pip3 install -r ./layers/my_layer/requirements.txt -t ./layers/my_layer/python


# Sharing lambda layers across stacks

While there are multiple ways to access a layer accross stacks, the BEST way to do this would be without duplicating the layer or generating additional versions of it. One way to achieve this is by sharing the ARN. This means building the layer in one infrastructure stack and exporting the ARN of the lambda layer. This exported ARN can later be accessed by other CDK stacks.


# Setup environment
Install the AWS CDK and setup authentication... not going to cover that here, but there are lots of resources on the web :)

Setup the python environment:

    python3 -m venv venv
    source ./venv/bin/activate

    pip3 install -r requirements.txt

# Deployment
Stacks can be deployed individually by providing their stack name:

    cdk deploy lambda-layers-example

or all at once:

    cdk deploy --all 