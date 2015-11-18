#!/bin/bash
for i in `./usernames.sh`; do ./delete-user.sh $i; done