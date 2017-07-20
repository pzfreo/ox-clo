#!/bin/bash 


eval $(docker-machine env $1-cass-1)
docker rm --force $(docker ps -aq)

eval $(docker-machine env $1-cass-2)
docker rm --force $(docker ps -aq)

eval $(docker-machine env $1-cass-3)
docker rm --force $(docker ps -aq)

eval $(docker-machine env $1-cass-4)
docker rm --force $(docker ps -aq)
