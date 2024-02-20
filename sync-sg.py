#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import logging
import helper
import os

# Get all running instances
running_instances = \
    helper.ec2_client.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# Call function to collect public address of running instances
public_ip_addresses = helper.get_public_ip_addresses(running_instances)

# Get current redshift security group allowed IPs
response = \
    helper.sg_client.describe_security_groups(GroupIds=[helper.redshift_sg_id])
current_rules = response['SecurityGroups'][0]['IpPermissions']
current_whitelisted_ips = []
for i in range(0, len(current_rules[0]['IpRanges'])):
    current_whitelisted_ips.append(current_rules[0]['IpRanges'][i]['CidrIp'])

# Populate lists for adding and removing IPs in redshift security group
helper.ips_to_add = [i for i in public_ip_addresses if i
                     not in current_whitelisted_ips]
helper.ips_to_remvove = [j for j in current_whitelisted_ips if j
                         not in public_ip_addresses]



def main():
    """
    Main function.
    """

    try:

        # Checking if any IPs need to be added or removed
        if set(helper.ips_to_add) == set(helper.ips_to_remvove):
            print('No modification is requred')
        else:
            # Removing obsolete ips from security group and keeping track of removed ips in rules.txt
            for i in helper.ips_to_remvove:
                helper.sg_client.revoke_security_group_ingress(GroupId=helper.redshift_sg_id,
                        IpPermissions=[{
                    'IpProtocol': 'tcp',
                    'FromPort': 5439,
                    'ToPort': 5439,
                    'IpRanges': [{'CidrIp': i}],
                    }])
                with open('rules.txt', 'w') as newfile:
                    newfile.write('IPs removed\n')
                    newfile.write(i)

            # Adding new ips to security group and keeping track of added ips in rules.txt
            for j in helper.ips_to_add:
                helper.sg_client.authorize_security_group_ingress(GroupId=helper.redshift_sg_id,
                        IpPermissions=[{
                    'IpProtocol': 'tcp',
                    'FromPort': 5439,
                    'ToPort': 5439,
                    'IpRanges': [{'CidrIp': j}],
                    }])
                with open('rules.txt', 'a') as newfile:
                    newfile.write('\nIPs added\n')
                    newfile.write(j)

            print('Security group updated successfully')
            helper.upload_to_s3('rules.txt')
            os.remove('rules.txt')
    
    except:
        logging.exception('')


if __name__ == '__main__':
    main()
