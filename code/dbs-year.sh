#!/bin/bash
for i in `./dates.sh 2017-07-01 2018-06-30`; do ./dbs.sh $i; done