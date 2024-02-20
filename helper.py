#!/usr/bin/env python3

import boto3
import os
import time

# EC2 client
ec2_client = boto3.resource("ec2", region_name="aws_region")

# Security group client
sg_client = boto3.client("ec2", region_name="aws_region")

# S3 client
s3_client = boto3.resource("s3")

# Security group
redshift_sg_id = "security_group_id"

# Create file with timestamp for logging to s3
timestr = time.strftime("%Y%m%d-%H%M%S")

# S3 bucket name for logging
s3_bucket_name = "your-bucket-name" + os.environ.get("env")
s3_path = timestr

# Initializing lists for adding and removing rules
ips_to_add = []
ips_to_remvove = []

# Function to collect public address
def get_public_ip_addresses(running_instances):
    ec2_public_ip_addresses = []
    for instance in running_instances:
        ec2_public_ip_addresses.append(instance.public_ip_address + "/32")
    return ec2_public_ip_addresses

# Function to upload logging file to s3
def upload_to_s3(file):
    s3_client.meta.client.upload_file('rules.txt', s3_bucket_name, timestr)
