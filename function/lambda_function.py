import os
import boto3
import json
import subprocess
import logging
from botocore.exceptions import ClientError
from aws_parameter_store import get_aws_parameter_store_value
from transfer_backup import transferbackup

os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['LAMBDA_TASK_ROOT']

try:
    bucket_name = os.environ['BUCKET']
except KeyError:
    bucket_name = ""
try:
    host = os.environ['DB_HOST']
except KeyError:
    host = ""
try:
    secret_name = os.environ['SECRET']
except KeyError:
    secret_name = ""
try:
    region_name = os.environ['REGION']
except KeyError:
    region_name = "eu-west-1"
try:
    username = os.environ['DB_USERNAME']
except KeyError:
    username = "root"
try:
    database = os.environ['DATABASE']
except KeyError:
    database = ""

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # Access AWS Systems Manager Parameter Store for root password
    password = get_aws_parameter_store_value(secret_name, region_name)

    # To execute the bash script on AWS Lambda, change its permissions and move it into the /tmp/ directory.
    # Source: https://stackoverflow.com/a/48196444
    subprocess.check_call(["cp ./backup.sh /tmp/backup.sh && chmod 755 /tmp/backup.sh"], shell=True)
    subprocess.check_call(["cp ./bin/mysqldump /tmp/mysqldump && chmod 755 /tmp/mysqldump"], shell=True)

    # Databases added as env vars, with  ':' used as delimiter
    databases = database.split(":")
    for db in databases:
        filename = db + '.sql'
        subprocess.check_call(["/tmp/backup.sh", host, username, password, database, filename])
        transferbackup(db, filename, bucket_name, region_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Backup Lambda Function finished successfully!')
    }
