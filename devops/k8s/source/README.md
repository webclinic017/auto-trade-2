# Deploying a service from source onto Kubernetes

https://katacoda.com/courses/kubernetes/deploy-service-from-source

## The container

```bash
export PATH=$PATH:~/.bin/ \
&& git clone https://github.com/datawire/hello-webapp.git \
&& export FORGE_SETUP_IMAGE=registry.hub.docker.com/datawire/forge-setup-test-katacoda:1 \
&& cat /proc/sys/kernel/random/uuid > hello-webapp/uuid.txt \
&& export LANG=C.UTF-8 && export LC_ALL=C.UTF-8
```

```bash
cd hello-webapp

cat Dockerfile

docker build -t hello-webapp:v1 .
```

## Running your containerized service

```bash
docker run -d -p 80:8080 hello-webapp:v1

curl host01
```

## Kubernetes and manifests

```bash
cat deployment.yaml
```

## The Container Registry

```bash
export REGISTRY=2886795316-5000-simba10.environments.katacoda.com

docker tag hello-webapp:v1 $REGISTRY/hello-webapp:v1

docker push $REGISTRY/hello-webapp:v1
```

## Running the service in Kubernetes

```bash
sed -i -e 's@IMAGE_URL@'"$REGISTRY/hello-webapp:v1"'@' deployment.yaml

cat deployment.yaml

scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@host01:/root/.kube/config ~/.kube/

kubectl apply -f deployment.yaml

kubectl get services

# Accessing the cluster
kubectl get pods
kubectl get svc

export PORT=$(kubectl get svc hello-webapp -o go-template='{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{"\n"}}{{end}}{{end}}')

curl host01:$PORT


```

## Automating the deployment process

```bash
sed -i -e 's/Hello World!/Hello Hacker News!!!/' app.py

# https://forge.sh/?utm_source=katacoda&utm_medium=tutorial&utm_campaign=tutorial
forge setup
# Docker Registry url
# 2886795272-5000-simba08.environments.katacoda.com
# Docker user
# root
# Docker password
# root
# Docker namespace/organization
# root

forge deploy

```

```bash
# set up a new port forward command
kubectl get pods

export PORT=$(kubectl get svc hello-webapp -o go-template='{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{"\n"}}{{end}}{{end}}')

curl host01:$PORT
```
