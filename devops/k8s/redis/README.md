# K8S & redis

## Redis Cluster

```bash 
# 准备好 k8s

# Master Replication Controller
kubectl create -f redis-master-controller.yaml
kubectl get rc
kubectl get pods

# Master Service
kubectl create -f redis-master-service.yaml
kubectl get services
kubectl describe services redis-master

# Slave Replication Pods
kubectl create -f redis-slave-controller.yaml
kubectl get rc

# Slave Service
kubectl create -f redis-slave-service.yaml
kubectl get services

# Frontend Replicated Pods
kubectl create -f frontend-controller.yaml
kubectl get rc
kubectl get pods

# Frontend Service
kubectl create -f frontend-service.yaml
kubectl get services

# Access Frontend
#   View Pods Status
kubectl get pods
#   Find NodePort
kubectl describe service frontend | grep NodePort
#   View UI
curl https://2886795285-30080-elsy06.environments.katacoda.com

```

## docker & Redis

```bash
mkdir -p ~/apps/redis/data
#写入redis默认配置
vim ~/apps/redis/redis.conf
#content
#bind 127.0.0.1 //允许远程连接
#protected-mode no
#appendonly yes //持久化
#requirepass 2419 //密码 

docker pull redis

docker run --name redis -p 6379:6379 \
-v ~/apps/redis/data:/data \
-v ~/apps/redis/redis.conf:/etc/redis.conf \
-d redis redis-server /etc/redis.conf --requirepass "123456"

docker exec -it redis redis-cli
```