#!/bin/bash 

./cass-1.sh $1 
./cass-n.sh $1 2 &
./cass-n.sh $1 3 &

wait
echo "cluster started"