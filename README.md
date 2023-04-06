# Background
This project implements two simple Lambda functions and a Lambda layer used by both. Using Lambda layers can be confusing and I'm going to attempt to help you sidestep some of the main pain points. The main issues I had when implementing this the first time were:

1. What is the best way to structure my Lambda layer into my existing project?
2. Why doesn't my Lambda function have access to the code in my Lambda layer?
3. How can I share the logic in my Lambda layer accross multiple stacks?

I'm going to attempt to answer #1 and #2 at this same time...

Directory structure
-------------------

AWS Lambda layers use a very specific directory structure because AWS Lambda will only look in a top level directory called "python" for python modules. Typically, if your function isn't able to access the modules you're providing in a layer, it's because the modules aren't in the `python` directory. Here's a simple example:

    -project-dir
      -layers
        -my-layer          <-- This directory is the entrypoint for the Lambda layer
          -python          <-- this directory *MUST* be named "python"
            my_layer.py    <-- custom module accessible through the layer

Now that you know what AWS expects of your code structure... how should you structure it into your codebase? The following example describes the code in this repo and follows best practices suggested by AWS. It is a bit more complicated but follows the same general concept. We separate Lambda layers into their own directories. Within those directories, we still collect *all* the Python modules that make up each layer into a subdirectory named `python`. That means one `python` directory per layer. In this example, I've created two Lambda layers; one is comprised of entirely external libraries (aka, modules we'll have to download or install), and the other is a module with local code.

    -lambda-layers-example
      app.py                   <-- Your CDK app which imports the stacks
      -layers
        infrastructure.py      <-- Just the lambda layer CDK infrastructure
        -external              <-- Layer of entirely external modules
          requirements.txt
          -python 
            flask              <-- Pip install your requirements here
            sqlalchemy
            jinja2
            ...
        -pythonutils           <-- A local code module
          -python
            -pythonutils       <-- *This* is the top level module we'll have access to
              __init__.py           from any attached Lambda function
              utildecorator.py <-- the logic we want to share between Lambdas
      -lambdamodule            <-- Application directory
        infrastructure.py      <-- Application infrastructure
        -runtime
          runtime.py           <-- Application logic

AWS Lambda `python` Directory
-----------------------------

So now you have an idea of how to organize your application based both on best practices and the requirements of AWS Lambda. If your Lambda function was unable to import the code from your layer, make sure your directory structure uses a `python` directory which is available at the top level of your layer.


Sharing Lambda layers across stacks
-----------------------------------

While there are multiple ways to access a layer accross stacks, the BEST way to do this is without duplicating the layer or generating additional versions of it. One way to achieve this is by sharing the ARN. This means building the layer in one infrastructure stack and exporting its ARN to make it available in downstream stacks. These downstream stacks can access the ARN and use it to attach the layer to a Lambda function without duplicating any resources.

Because the layer stack is now a dependency for any downstream stacks using the ARN of the layer, you must implement `add_dependency` to your CDK app to ensure correct deployment order.


# Setup environment
Install the AWS CDK and setup authentication... not going to cover that here, but there are lots of resources on the web :)

Setup the python environment:

    python3 -m venv venv
    source ./venv/bin/activate

    pip3 install -r requirements.txt

# Build

Because one of our Lambda layers uses external libraries, we have to include a build step in the development workflow. The purpose of this step is to download the dependencies for any Lambda layer and to move them into a location where they'll be accessible after deployment. Putting build logic into a shell script gives you less to remember. I find it useful even if the build is a single line, like it is in this case. Check it out in `./scripts/build.sh`. When you're ready to build the external layer, execute it.

    ./scripts/build.sh

# Deployment


Stacks can be deployed individually by providing their stack name:

    cdk deploy Lambda-layers-example

or all at once:

    cdk deploy --all 