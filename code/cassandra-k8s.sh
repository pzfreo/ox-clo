# kubernetes cassandra demo

# 1. create a k8s cluster with 2 nodes

gcloud container clusters create cassandra-cluster --num-nodes=2 --machine-type=n1-standard-2
# wait a bit


# configure kubectl to use the cluster

kubectl apply -f cassandra-service.yaml
kubectl get all

kubectl apply -f cassandra-statefulset.yaml
kubectl get all

# Show k9s

kubectl exec -ti cassandra-0 -- nodetool status

# Wait until ready

kubectl exec -ti cassandra-0 -- cassandra-stress write n=100000 -rate threads=1000


gcloud container clusters resize cassandra-cluster --node-pool default-pool --num-nodes 4

kubectl scale --replicas 6 statefulset/cassandra

kubectl exec -ti cassandra-0 -- nodetool status

# Wait until ready

kubectl exec -ti cassandra-0 -- cassandra-stress write n=100000 -rate threads=1000
