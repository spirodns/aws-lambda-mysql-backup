#!/usr/bin/env bash
# Perform a MySQL database dump to back up the database
# Sources: [https://mariadb.com/kb/en/library/mysqldump/]
# Input Variables
HOST=$1
USERNAME=$2
PASSWORD=$3
DATABASE=$4
FILENAME=$5

# Use an environment variable for the MySQL password so that mysqldump doesn't have to prompt for one.
export MYSQL_PWD="${PASSWORD}"
# Dump the database into a sql file
/tmp/mysqldump -v --host ${HOST} --user ${USERNAME} --ssl --max_allowed_packet=1G --single-transaction --quick \
    --lock-tables=false --routines ${DATABASE} > /tmp/${FILENAME}


