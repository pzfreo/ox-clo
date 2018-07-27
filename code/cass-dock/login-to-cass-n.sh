#! /bin/bash

eval $(docker-machine env $1-cass-$2)
docker exec -ti cassandra-$2 /bin/bash