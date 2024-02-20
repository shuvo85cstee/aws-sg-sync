# aws-sg-sync
This service will add rules to whitelist public ips of running EKS worker nodes in Redshift security.<br />
It will also remvove rules from redshift security group when ips of EKS nodes which are no longer active.<br />
All rules modifications will be logged in S3.
