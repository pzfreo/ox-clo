#!/bin/bash
set -e -x
aws iam create-user --user-name $1
aws iam create-login-profile --password-reset-required --user-name $1 --password $1
aws iam add-user-to-group --user-name $1 --group-name students

