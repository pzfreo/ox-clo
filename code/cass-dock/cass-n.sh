#!/bin/bash 
set -x

CASSIMG="jnummelin/weave-cassandra:3.0"

eval $(docker-machine env $1-cass-$2)
docker rm --force $(docker ps -aq)
weave launch $(docker-machine ip $1-cass-1) --password weavepass
eval $(weave env)

docker run --name cassandra-$2 -d -e CASSANDRA_LISTEN_ADDRESS=weave -e CASSANDRA_BROADCAST_ADDRESS=weave -e CASSANDRA_SEEDS=cassandra-1.weave.local $CASSIMG
