#!/bin/bash 

#sudo curl -L git.io/weave -o /usr/local/bin/weave
#sudo chmod a+x /usr/local/bin/weave

CASSIMG="jnummelin/weave-cassandra:3.0"
AWSMACH="m3.medium"
AWSREG="eu-west-1"
DM_OPTS="-d amazonec2 --amazonec2-region $AWSREG --amazonec2-instance-type $AWSMACH --engine-install-url=https://freo.me/getdocker --amazonec2-open-port 6783 --amazonec2-open-port 6784 --amazonec2-open-port 12375"


docker-machine rm --force $1-cass-1
aws ec2 delete-key-pair --key-name $1-cass-1
docker-machine rm --force $1-cass-2
aws ec2 delete-key-pair --key-name $1-cass-2
docker-machine rm --force $1-cass-3
aws ec2 delete-key-pair --key-name $1-cass-3
docker-machine rm --force $1-cass-4
aws ec2 delete-key-pair --key-name $1-cass-4

docker-machine create $DM_OPTS $1-cass-1
docker-machine create $DM_OPTS $1-cass-2

eval $(docker-machine env $1-cass-1)
CASS1IP=$(docker-machine ip $1-cass-1)
weave launch --password weavepass
eval $(weave env)


docker run --name cassandra-1 -d -e CASSANDRA_LISTEN_ADDRESS=weave -e CASSANDRA_BROADCAST_ADDRESS=weave $CASSIMG


docker-machine create $DM_OPTS $1-cass-2
eval $(docker-machine env $1-cass-2)
weave launch $CASS1IP --password weavepass
eval $(weave env)

docker run --name cassandra-2 -d -e CASSANDRA_LISTEN_ADDRESS=weave -e CASSANDRA_BROADCAST_ADDRESS=weave -e CASSANDRA_SEEDS=cassandra-1.weave.local $CASSIMG


docker-machine create $DM_OPTS $1-cass-3
eval $(docker-machine env $1-cass-3)
weave launch $CASS1IP --password weavepass
eval $(weave env)

docker run --name cassandra-3 -d -e CASSANDRA_LISTEN_ADDRESS=weave -e CASSANDRA_BROADCAST_ADDRESS=weave -e CASSANDRA_SEEDS=cassandra-1.weave.local $CASSIMG


