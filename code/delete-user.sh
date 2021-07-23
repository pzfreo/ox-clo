#!/bin/bash
set -e -x
aws iam delete-login-profile --user-name $1 || true
aws iam remove-user-from-group --user-name $1 --group-name students || true
aws iam delete-access-key --user-name $1 --access-key-id $(aws iam list-access-keys --user-name $1 | jq -r .AccessKeyMetadata[0].AccessKeyId) || true
aws iam delete-access-key --user-name $1 --access-key-id $(aws iam list-access-keys --user-name $1 | jq -r .AccessKeyMetadata[0].AccessKeyId) || true
aws iam delete-user --user-name $1 || true

