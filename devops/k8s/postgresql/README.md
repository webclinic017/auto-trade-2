# K8S & pg

https://www.sumologic.com/blog/kubernetes-deploy-postgres/

https://juejin.cn/post/6844904094272847885

https://hanggi.me/post/kubernetes/k8s-postgresql/

https://www.modb.pro/db/102116

## password

```sh
echo "password" | base64

# cGFzc3dvcmQK
```

## postgres-secrets.yaml

```sh
# 创建 postgres-secrets.yaml
cat postgres-secrets.yaml

```

```yaml
apiVersion: v1
kind: Secret
metadata:
    name: postgres-secret-config
type: Opaque
data:
    password: cG9zdGdyZXMK
```

```sh
# k8s 执行
kubectl apply -f postgres-secrets.yaml

# secret/postgres-secret-config created
```

```sh
# 查看
kubectl get secret postgres-secret-config -o yaml

# apiVersion: v1
# kind: Secret
# metadata:
#     name: postgres-secret-config
# type: Opaque
# data:
#    password: cG9zdGdyZXMK
```

## 创建 PersistentVolume 和 PersistentVolumeClaim

- pv volume

```sh
cat pv-volume.yaml
```

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
    name: postgres-pv-volume
    labels:
        type: local
spec:
    storageClassName: manual
    capacity:
        storage: 5Gi
    accessModes:
        - ReadWriteOnce
    hostPath:
        path: "/mnt/data"
```

```sh
kubectl apply -f pv-volume.yaml

# persistentvolume/postgres-pv-volume created
```

```sh
# 查看 pv
kubectl get pv postgres-pv-volume
```

- pv-claim volume

```sh
cat pv-claim.yaml
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
    name: postgres-pv-claim
spec:
    storageClassName: manual
    accessModes:
        - ReadWriteOnce
    resources:
        requests:
            storage: 1Gi
```

```sh
kubectl apply -f pv-claim.yaml

# persistentvolumeclaim/postgres-pv-claim created
```

```sh
# 查看 pvc
kubectl get pvc postgres-pv-claim
```

## 创建 Demployment

```sh
cat postgres-deployment.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      volumes:
        - name: postgres-pv-storage
          persistentVolumeClaim:
            claimName: postgres-pv-claim
      containers:
        - name: postgres
          image: postgres:11
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret-config
                  key: password
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          volumeMounts:
            - mountPath: /var/lib/postgresql/data
              name: postgres-pv-storage
```

```sh
# k8s 执行
kubectl apply -f postgres-deployment.yaml

# deployment.apps/postgres created

# 查看 deployments
kubectl get deployments
```

## 创建 service

```sh
cat postgres-service.yaml

# <node_server_ip>:<node_port> 访问
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  labels:
    app: postgres
spec:
  type: NodePort
  ports:
    - port: 5432
  selector:
    app: postgres
```

```sh
# Create a cluster, mapping the port 30032 from agent-0 to localhost:8432
# k3d cluster create postgrescluster -p "8432:30032@agent:0" --agents 2

# k8s 执行
kubectl apply -f postgres-service.yaml

# service/postgres created

# 查看 service
kubectl get service postgres
```

## 测试数据库连接

```sh
# 查看 pods
kubectl get pods

# NAME READY STATUS RESTARTS AGE
# postgres-59f958ccd8-j6mbq 1/1 Running 0 2m12s

kubectl exec -it postgres-59f958ccd8-j6mbq -- psql -U postgres
```

```sh
# 手动方式
POD=`kubectl get pods -l app=postgres -o wide | grep -v NAME | awk '{print $1}'`
```


```sh
# 用另一个 docker 容器通过 psql 连接

# 密码
export POSTGRES_PASSWORD=$(kubectl get secret postgres-secret-config -o jsonpath="{.data.password}" | base64 --decode)

# 连接
kubectl run postgres-client --rm --tty -i --restart='Never' --image postgres:11 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql -h postgres -U postgres

# 连接成功即可执行查询
# SELECT * FROM pg_database;
# https://www.cnblogs.com/zszxz/p/12222201.html


# 另外
lsof -i :8032
kill -9 12345

kubectl get namespaces
kubectl get pods
kubectl --namespace default port-forward pods/postgres-59f958ccd8-j6mbq 8032:5432&

psql -h localhost -U postgres --password -p 8032 postgresdb

# 安装 psycopg2
pip3 install psycopg2 -i https://pypi.tuna.tsinghua.edu.cn/simple
# 如果 报错 pg_config executable not found
# sudo apt-get install libpq-dev python-dev
brew install postgresql
pip3 install psycopg2-binary


# https://katacoda.com/

# Katacoda专注于Cloud Native应用程序，其中包括Kubernetes以及许多其他项目和技术。这是学习有关许多主题的交互式教程的好地方，其中包括：

# - Kubernetes和相关技术
# - 无服务器
# - terraform
# - 机器学习
# - 编程语言：Go，Ruby，Node.Js，Python，Kotlin等
# - Linux
# - …


```

## 下一步： Advanced PostgreSQL Deployment

- 调整 PersistentVolume policy，防止用户删除 pvc volumes 时自动删除 pv volumes

- PostgreSQL 集群，高可用，横向扩展，弹性伸缩，自动修复（Automated failover），自动恢复，备份，智能回滚更新

Crunchy PostgreSQL Operator，Zalando Postgres Operator


