# aws-lambda-rds-backup (Python)

The project source includes function code and supporting resources:

- `function` - A Python function.
- `template.yml` - An AWS CloudFormation template that creates an application.
- `1-create-bucket.sh`, `2-deploy.sh`, etc. - Shell scripts that use the AWS CLI to deploy and manage the application.

Use the following instructions to deploy the sample application.

# Requirements
- [Python 3.7](https://www.python.org/downloads/)
- The Bash shell. For Linux and macOS, this is included by default. In Windows 10, you can install the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to get a Windows-integrated version of Ubuntu and Bash.
- [The AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) v1.17 or newer.

If you use the AWS CLI v2, add the following to your [configuration file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) (`~/.aws/config`):

```
cli_binary_format=raw-in-base64-out
```

This setting enables the AWS CLI v2 to load JSON events from a file, matching the v1 behavior.

# Setup
Download or clone this repository.
Add in the `template.yml` file the required values for the parameters listed:

    DbHost:
    DbUsername:
    ParameterStoreSecret:
    Database:
    BucketName:
    Region:
    CronjobRule:
    RDSSubnetIdA:
    RDSSubnetIdB:
    RouteTableA:
    RouteTableB:
    DefaultSecurityGroupId:
    RDSSecurityGroupId:
    VPCID:
The variables `DbHost`,`DbUsername`,`BucketName`,`Region`,`Database` are mapped as Environmental Variables for the Lambda Function, thus they can also change on the fly.
Values for the `Database` variable can contain more than one(1) databases, with the use of a column (:) as delimiter.


This function uses extra libraries for the `mysqldump` binary. This are uploaded from the `package` folder to a S3 buckets for deployments artifacts.
Create a new bucket for deployment artifacts, run `1-create-bucket.sh`.

    $ ./1-create-bucket.sh
    make_bucket: lambda-artifacts-a5e491dbb5b22e0d


# Deploy
To deploy the application, run `2-deploy.sh`.

    $ ./2-deploy.sh
    Uploading to e678bc216e6a0d510d661ca9ae2fd941  9519118 / 9519118.0  (100.00%)
    Successfully packaged artifacts and wrote output template to file out.yml.
    Waiting for changeset to be created..
    Waiting for stack create/update to complete
    Successfully created/updated stack - blank-python

This script uses AWS CloudFormation to deploy the Lambda function, IAM role with specific policies, an S3 Bucket for storage, an VPC endpoint for S3 access and a VPC endpoint for SSM. If the AWS CloudFormation stack that contains the resources already exists, the script updates it with any changes to the template or function code.

# Test
To invoke the function, run `3-invoke.sh`.

    $ ./3-invoke.sh
    {
        "StatusCode": 200,
        "ExecutedVersion": "$LATEST"
    }
    {"TotalCodeSize": 410713698, "FunctionCount": 45}

Let the script invoke the function a few times and then press `CRTL+C` to exit.


# Cleanup
To delete the application, run `4-cleanup.sh`.

    $ ./4-cleanup.sh
