#!/bin/bash
aws ec2 describe-instances --filters Name=instance-state-code,Values=16 --query Reservations[].Instances[].InstanceId
