# Running Stateful Services on Kubernetes

## Deploy NFS Server

```bash
docker run -d --net=host \
   --privileged --name nfs-server \
   katacoda/contained-nfs-server:centos7 \
   /exports/data-0001 /exports/data-0002
```

##  pv

```bash
# Deploy Persistent Volume
kubectl create -f nfs-0001.yaml
kubectl create -f nfs-0002.yaml
cat nfs-0001.yaml nfs-0002.yaml

# Deploy Persistent Volume Claim
kubectl get pv
```

## pvc

```bash
kubectl create -f pvc-mysql.yaml
kubectl create -f pvc-http.yaml
cat pvc-mysql.yaml pvc-http.yaml
kubectl get pvc
```

## use pv

```bash
kubectl create -f pod-mysql.yaml
kubectl create -f pod-www.yaml
cat pod-mysql.yaml pod-www.yaml
kubectl get pods
```

## Read / Write Data

```bash
docker exec -it nfs-server bash -c "echo 'Hello World' > /exports/data-0001/index.html"

ip=$(kubectl get pod www -o yaml |grep podIP | awk '{split($0,a,":"); print a[2]}'); echo $ip
curl $ip

# Update Data

docker exec -it nfs-server bash -c "echo 'Hello NFS World' > /exports/data-0001/index.html"
curl $ip

```

## Recreate Pod

```bash
kubectl delete pod www

kubectl create -f pod-www2.yaml

ip=$(kubectl get pod www2 -o yaml |grep podIP | awk '{split($0,a,":"); print a[2]}'); curl $ip
```

