#!/bin/bash
set -eo pipefail
STACK_NAME=$1
FUNCTION=$(aws cloudformation describe-stack-resource --stack-name $STACK_NAME --logical-resource-id function --query 'StackResourceDetail.PhysicalResourceId' --output text)


aws lambda invoke --function-name $FUNCTION --payload file://event.json out.json
