#!/bin/bash 

AWSMACH="m3.medium"
AWSREG="eu-west-1"
DM_OPTS="-d amazonec2 --amazonec2-region $AWSREG --amazonec2-instance-type $AWSMACH --engine-install-url=https://freo.me/getdocker --amazonec2-open-port 6783 --amazonec2-open-port 6784 --amazonec2-open-port 12375"

#DIGMACH="4Gb"
#DIGREG="lon1"
#DM_OPTS="-d digitalocean --digitalocean-region=$DIGREG --digitalocean-size=$DIGMACH  --digitalocean-access-token=$DIGOCTOK  --digitalocean-image ubuntu-14-04-x64"

set -x

docker-machine rm --force $1-cass-1
# aws ec2 delete-key-pair --key-name $1-cass-1
docker-machine rm --force $1-cass-2
# aws ec2 delete-key-pair --key-name $1-cass-2
docker-machine rm --force $1-cass-3
# aws ec2 delete-key-pair --key-name $1-cass-3
docker-machine rm --force $1-cass-4
# aws ec2 delete-key-pair --key-name $1-cass-4

docker-machine create $DM_OPTS $1-cass-1 & 
docker-machine create $DM_OPTS $1-cass-2 & 
docker-machine create $DM_OPTS $1-cass-3 & 
docker-machine create $DM_OPTS $1-cass-4 &

wait
echo "Machines are ready"