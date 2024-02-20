# aws-sg-sync
We need to update redshift security group regularly to match the current public IPs of running EC2 instances.
This script will add new IPs and remove IPs no longer needed in security group.
It will also logs all changes in security group to s3 for audit.
