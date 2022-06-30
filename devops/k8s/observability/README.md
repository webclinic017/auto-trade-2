# Kubernetes Observability: Basics

https://katacoda.com/courses/kubernetes/kubernetes-observability-basics-by-javajon

## Your Kubernetes Cluster

```bash
# Your Kubernetes Cluster
kubectl version --short && \
kubectl get componentstatus && \
kubectl get nodes && \
kubectl cluster-info

helm version --short

# Kubernetes Dashboard
k8s-dash-token.sh
```

## Sample Application

```bash
kubectl create deployment random-logger --image=chentex/random-logger

kubectl scale deployment/random-logger --replicas=3

kubectl get pods

```

## Resource Inspection

```bash
# General Inspection of a Cluster
kubectl cluster-info

kubectl describe node node01

kubectl cluster-info dump --all-namespaces --output-directory=cluster-state --output=j

tree cluster-state

jq '.items[]?.status.containerStatuses[]?.image' cluster-state/kube-system/pods.json

jq '.items[]?.status.containerStatuses[]? | [.image, .state[]?.startedAt]' cluster-state/default/pods.json

# General Inspection for a Deployment
kubectl describe deployment random-logger
kubectl describe deployments | grep "Replicas:"

kubectl get pods
kubectl describe pods

# Events
kubectl get events
kubectl scale deployment/random-logger --replicas=2

kubectl get events --sort-by=.metadata.creationTimestamp

# Inspecting Containers
POD=$(kubectl get pod  -o jsonpath="{.items[0].metadata.name}")

kubectl exec $POD -- cat entrypoint.sh

kubectl exec -it $POD -- /bin/sh
# and come back out with the exit command.

kubectl exec $POD -- uptime

kubectl exec $POD -- ps

kubectl exec $POD -- stat -f /

kubectl exec $POD --container random-logger -- lsof

kubectl exec $POD --container random-logger -- iostat

# When the Pod has more than one container, the specific container name may be referenced.
kubectl exec $POD --container random-logger -- ls -a -l


```

```bash 
controlplane $ tree cluster-state
cluster-state
├── default
│   ├── daemonsets.json
│   ├── deployments.json
│   ├── events.json
│   ├── pods.json
│   ├── random-logger-7687d48b59-fwz6c
│   │   └── logs.txt
│   ├── random-logger-7687d48b59-jsvqn
│   │   └── logs.txt
│   ├── random-logger-7687d48b59-kjg7p
│   │   └── logs.txt
│   ├── replicasets.json
│   ├── replication-controllers.json
│   └── services.json
├── kube-node-lease
│   ├── daemonsets.json
│   ├── deployments.json
│   ├── events.json
│   ├── pods.json
│   ├── replicasets.json
│   ├── replication-controllers.json
│   └── services.json
├── kube-public
│   ├── daemonsets.json
│   ├── deployments.json
│   ├── events.json
│   ├── pods.json
│   ├── replicasets.json
│   ├── replication-controllers.json
│   └── services.json
├── kube-system
│   ├── coredns-66bff467f8-q5wrt
│   │   └── logs.txt
│   ├── coredns-66bff467f8-zhgzs
│   │   └── logs.txt
│   ├── daemonsets.json
│   ├── deployments.json
│   ├── etcd-controlplane
│   │   └── logs.txt
│   ├── events.json
│   ├── katacoda-cloud-provider-5b7d86c4d7-9pr2s
│   │   └── logs.txt
│   ├── kube-apiserver-controlplane
│   │   └── logs.txt
│   ├── kube-controller-manager-controlplane
│   │   └── logs.txt
│   ├── kube-flannel-ds-amd64-7lw8m
│   │   └── logs.txt
│   ├── kube-flannel-ds-amd64-bbkps
│   │   └── logs.txt
│   ├── kube-keepalived-vip-qr4m2
│   │   └── logs.txt
│   ├── kube-proxy-s658w
│   │   └── logs.txt
│   ├── kube-proxy-w2fw6
│   │   └── logs.txt
│   ├── kube-scheduler-controlplane
│   │   └── logs.txt
│   ├── pods.json
│   ├── replicasets.json
│   ├── replication-controllers.json
│   └── services.json
└── nodes.json
```

## cAdvisor

```bash

kubectl get nodes

export NODE_0=$(kubectl get nodes -o=jsonpath="{.items[0].metadata.name}")

export NODE_1=$(kubectl get nodes -o=jsonpath="{.items[1].metadata.name}")

echo -e "The control-plane node is $NODE_0 \nThe worker node is $NODE_1"

kubectl proxy > /dev/null &

curl localhost:8001/api/v1/nodes/$NODE_0/proxy/metrics

curl localhost:8001/api/v1/nodes/$NODE_1/proxy/metrics

curl localhost:8001/metrics/ | jq
```

## Metrics Server

```bash
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes | jq

kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes/node01 | jq

kubectl top node

kubectl top pods --all-namespaces
```