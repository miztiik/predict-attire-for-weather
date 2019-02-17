#!/bin/bash
set -x
set -e 
# steps taken verbatim from:
#  http://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html#install_docker
#
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Also install some common sense stuff
sudo yum install -y git
sudo yum -y groupinstall "Development Tools"

# log out and log in to pickup the added group
source ~/.bash_profile