#!/bin/bash
for i in `./usernames.sh`; do ./create-user.sh $i; done