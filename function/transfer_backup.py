import boto3
import botocore.config
import logging
from os import path
from datetime import datetime

def transferbackup(database, filename, bucket_name, region_name):
    ###implementing weekly, monthly, daily backups
    now = datetime.now()
    # Day of the month as a zero-padded decimal number.
    day_of_the_month = now.strftime("%d")
    # Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.
    day_of_the_week_number = now.strftime("%w")
    weekday = now.strftime("%A")
    month = now.strftime("%B")
    # Week number of the year (Sunday as the first day of the week) as a zero padded decimal number.
    week_number = now.strftime("%U")

    # By default, S3 resolves buckets using the internet.  To use the VPC endpoint instead, use the 'path' addressing
    # style config.  Source: https://stackoverflow.com/a/44478894
    s3 = boto3.resource('s3', region_name, config=botocore.config.Config(s3={'addressing_style': 'path'}))

    if path.exists('/tmp/' + filename):
        # Upload the file
        if day_of_the_month == '01':
            try:
                s3.meta.client.upload_file('/tmp/' + filename, bucket_name, 'monthly/' + month + '/' + filename)
                logging.info("Monthly backup for database: %s for month: %s", database, month)
            except ClientError as e:
                logging.error(e)
        if day_of_the_week_number == '6':
            try:
                s3.meta.client.upload_file('/tmp/' + filename, bucket_name, 'weekly/' + week_number + '/' + filename)
                logging.info("Weekly backup for database: %s for month: %s", database, month)
            except ClientError as e:
                logging.error(e)
        try:
            s3.meta.client.upload_file('/tmp/' + filename, bucket_name, 'daily/' + weekday + '/' + filename)
            logging.info("Daily backup for database: %s for weekday: %s", database, weekday)
        except ClientError as e:
            logging.error(e)
            return False
    return True