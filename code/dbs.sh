#!/bin/bash
set -e -x
aws s3 cp s3://deutsche-boerse-xetra-pds/$1/ s3://oxclo-dbs/ --include "*.csv" --recursive