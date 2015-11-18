#!/bin/bash
set -e -x
aws iam delete-login-profile --user-name $1 || true
aws iam remove-user-from-group --user-name $1 --group-name students || true
aws iam delete-user --user-name $1 || true

