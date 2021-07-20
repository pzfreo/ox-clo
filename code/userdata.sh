#!/bin/bash
# verbosity
set -e -x
# update the package list
apt-get update
apt-get install curl -y
curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash - 
# install node, node package manager and git.
apt-get update
apt-get -y install nodejs
cd /home/ubuntu
# use git to copy the node.js code into the system
git clone https://github.com/pzfreo/auto-deploy-node-js.git
cd auto-deploy-node-js
npm install
# pass the DB connection parameters into the code
export DBURL=oxclo.cluster-citfamc1edxs.eu-west-1.rds.amazonaws.com
export DBUSER=node
export DBPW=node
# start the server as a daemon
npm start
#that's all