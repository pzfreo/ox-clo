#!/bin/bash
# verbosity
set -e -x
# update the package list
apt-get update
# install node, node package manager and git.
apt-get -y install build-essential git autotools-dev autoconf
cd /home/ubuntu && git clone https://github.com/JoeDog/siege.git && cd siege  && utils/bootstrap && ./configure && sed -i -e 's/verbose = true/verbose = false/g' utils/siege.config && make && make install
# set more file descriptors
echo "* hard nofile 64000" >> /etc/security/limits.conf
echo "* soft nofile 64000" >> /etc/security/limits.conf
