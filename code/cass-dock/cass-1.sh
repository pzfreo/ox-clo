#!/bin/bash 

set -x

CASSIMG="jnummelin/weave-cassandra:3.0"

eval $(docker-machine env $1-cass-1)
docker rm --force $(docker ps -aq)

weave launch --password weavepass
eval $(weave env)
docker run --name cassandra-1 -e CASSANDRA_LISTEN_ADDRESS=weave -e CASSANDRA_BROADCAST_ADDRESS=weave $CASSIMG
