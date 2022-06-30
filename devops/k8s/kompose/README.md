# Deploy Docker Compose with Kompose

## Install

```bash
curl -L https://github.com/kubernetes/kompose/releases/download/v1.9.0/kompose-linux-amd64 -o /usr/bin/kompose && chmod +x /usr/bin/kompose
```

## kompose up

```bash
kompose up
kubectl get deployment,svc,pods,pvc
```

## Convert

```bash
kompose convert

ls
```

## Kubectl create

```bash
kubectl apply -f frontend-service.yaml,redis-master-service.yaml,redis-slave-service.yaml,frontend-deployment.yaml,redis-master-deployment.yaml,redis-slave-deployment.yaml
```

## OpenShift

Kompose also supports different Kubernetes distributions, for example OpenShift.

```bash
kompose --provider openshift convert
```

## Convert To Json

```bash
kompose convert -j
```

