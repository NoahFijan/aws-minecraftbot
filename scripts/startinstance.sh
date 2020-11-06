#!/bin/bash
aws ec2 start-instances --instance-ids $1 >/dev/null
aws ec2 wait instance-running --instance-ids $1
aws ec2 describe-instances --instance-ids $1 --query "Reservations[].Instances[].PublicIpAddress" --output=text
#TODO
#ssh or something similar into the vm and start
#the minecraft server application
