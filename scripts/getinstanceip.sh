#!/bin/bash
#echo $1
aws ec2 describe-instances  --instance-ids $1 --query "Reservations[].Instances[].PublicIpAddress" --output=text
