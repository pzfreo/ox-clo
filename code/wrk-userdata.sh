#!/bin/bash
# verbosity
set -e -x
# update the package list
apt-get update
# install node, node package manager and git.
sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install build-essential libssl-dev git
cd /home/ubuntu 
git clone https://github.com/wg/wrk.git wrk
cd wrk
make
sudo cp wrk /usr/local/bin
# set more file descriptors
echo "* hard nofile 64000" >> /etc/security/limits.conf
echo "* soft nofile 64000" >> /etc/security/limits.conf
