for i in $(aws sns list-subscriptions | jq .Subscriptions[].SubscriptionArn | cut -d\" -f2 ) ; do  aws sns unsubscribe --subscription-arn $i ; done

for i in $(aws sns list-topics | jq .Topics[].TopicArn | cut -d\" -f2 ) ; do  aws sns delete-topic --topic-arn $i ; done