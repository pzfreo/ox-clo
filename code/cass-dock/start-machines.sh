#!/bin/bash 

AWSMACH="m3.medium"
AWSREG="eu-west-1"
DM_OPTS="-d amazonec2 --amazonec2-region $AWSREG --amazonec2-instance-type $AWSMACH --amazonec2-open-port 6783 --amazonec2-open-port 6784 --amazonec2-open-port 12375"

#DIGMACH="4Gb"
#DIGREG="lon1"
#DM_OPTS="-d digitalocean --digitalocean-region=$DIGREG --digitalocean-size=$DIGMACH  --digitalocean-access-token=$DIGOCTOK  --digitalocean-image ubuntu-14-04-x64"

set -x


docker-machine create $DM_OPTS $1-cass-1 & 
docker-machine create $DM_OPTS $1-cass-2 & 
docker-machine create $DM_OPTS $1-cass-3 & 
docker-machine create $DM_OPTS $1-cass-4 &

wait
echo "Machines are ready"