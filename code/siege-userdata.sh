#!/bin/bash
# verbosity
set -e -x
# update the package list
apt-get update
apt-get install build-essential wget
# install node, node package manager and git.
wget http://download.joedog.org/siege/siege-4.0.2.tar.gz
tar xzvf siege-4.0.2.tar.gz
cd siege-4.0.2
configure && make && make install
# set more file descriptors
echo "* hard nofile 64000" >> /etc/security/limits.conf
echo "* soft nofile 64000" >> /etc/security/limits.conf
