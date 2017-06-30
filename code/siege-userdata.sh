#!/bin/bash
# verbosity
set -e -x
# update the package list
apt-get update
# install siege
apt-get -y install build-essential git autotools-dev autoconf
cd /home/ubuntu && git clone https://github.com/JoeDog/siege.git && cd siege && utils/bootstrap && ./configure && make && make install
# set more file descriptors
echo "* hard nofile 64000" >> /etc/security/limits.conf
echo "* soft nofile 64000" >> /etc/security/limits.conf
