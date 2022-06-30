# DevOps

https://github.com/jfeng45/k8sdemo

## K8S

```bash
# mac
# https://xkcoding.com/2021/03/15/run-local-k8s-cluster-quickly.html

brew install --cask docker
brew install k3d
brew install kubectl
brew install kubecm

# 配置docker.io镜像加速
# 创建registries.yaml文件
sudo tee registries.yaml >> EOF
mirrors:
  "docker.io":
    endpoint:
      - "https://fogjl973.mirror.aliyuncs.com"
      - "https://docker.mirrors.ustc.edu.cn"
      - "https://registry-1.docker.io"
EOF

# 首先我们尝试创建一个 1主2从 的集群：
k3d cluster create first-cluster --port 8080:80@loadbalancer --port 8443:443@loadbalancer --api-port 6443 --servers 1 --agents 2

# 或者 高可用集群
k3d cluster create --servers 3 --image rancher/k3s:v1.19.3-k3s2

# 或者
docker run -d --restart=always --name rancher -p 80:80 -p 443:443 --privileged rancher/rancher:v2.5.12

# 查看下当前集群的信息
kubectl cluster-info

# 查看下当前集群的节点情况
kubectl get nodes

# “节点” 其实是本机 Docker 运行的容器，通过 docker ps 查看下当前本机运行的容器
docker ps

# 停止集群：
k3d cluster stop first-cluster

# 重启集群：
k3d cluster start first-cluster

# 删除集群：
k3d cluster delete first-cluster

# 指定版本号：
k3d cluster create first-cluster xxxxx --image rancher/k3s:v1.19.8-k3s1

# 快速切换 kubectl context
kubecm s

# 测试 nginx
kubectl create deployment nginx --image=nginx

kubectl create service clusterip nginx --tcp=80:80

cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx
  annotations:
    ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx
            port:
              number: 80
EOF

# 打开 http://localhost:8080/

```

```bash
# Docker 部署 mysql
mkdir -p ~/apps/mysql/data ~/apps/mysql/logs ~/apps/mysql/conf
# docker pull daocloud.io/library/mysql:5.7
docker pull mysql:5.7
docker run -p 3306:3306 --name mysql \
-v ~/apps/mysql/conf:/etc/mysql/conf.d \
-v ~/apps/mysql/logs:/logs \
-v ~/apps/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7

docker exec -it mysql mysql -u root -p123456
grant all privileges on *.* to root@'%' identified by '123456';
flush privileges;

# Docker 部署 redis
mkdir -p ~/apps/redis/data
# 写入 redis 默认配置
vim ~/apps/redis/redis.conf

docker pull redis
docker run --name redis -p 6379:6379 -v ~/apps/redis/data:/data -v ~/apps/redis/redis.conf:/etc/redis.conf -d redis redis-server /etc/redis.conf --requirepass "123456"
docker exec -it redis redis-cli
```

### K8S & MySQL

- 创建 Deployment 和 Service：

```bash
kubectl apply -f k8s/mysql/mysql-deployment.yaml
kubectl apply -f k8s/mysql/mysql-service.yaml
```

- 查看 Service

```
kubectl get service
```

- MySQL 连接

```
mysql -h localhost -P 30306 --protocol=tcp -u root -p
```

- 宿主机网络 & 虚拟机网路 & k8s 集群内部网络

LoadBalancer， NodePort，ClusterIP, Ingress

- 卷（volume）：

卷是k8s的存储概念，它依附于Pod，不能单独存在。但它不是在容器层。因此如果容器被重新启动，卷仍然在。但如果Pod重新启动，卷就丢失了。如果一个Pod里有多个容器，那么这些容器共享Pod的卷。你可以把卷看成是一个目录，里面可以存储各种文件。k8s支持各种类型的卷，例如本地文件系统和各种云存储。

- 持久卷（PersistentVolume）：

是对卷的一个封装，目的是为了更好地管理卷。它的生命周期不需要与Pod绑定，它可以独立于Pod存在。

- 持久卷申请（PersistentVolumeClaim）：

是对持久卷资源的一个申请，你可以申请特定的存储容量的大小和访问模式，例如读写模式或只读模式。k8s会根据持久卷申请分配适合的持久卷，如果没有合适的，系统会自动创建一个。持久卷申请是对持久卷的一个抽象，就像编程里的接口（Interface）,它可以有不同的具体实现（持久卷）。例如，阿里云和华为云支持的存储系统不同，它生成的持久卷也不相同。持久卷是与特定的存储实现绑定的。那你要把程序从阿里云移植到华为云，怎么保证配置文件的兼容性呢？你就用持久卷申请来做这个接口，它只规定存储容量大小和访问模式，而由阿里云和华为云自动生成各自云里满足这个接口需求的持久卷. 不过，它还有一个限制条件，那就是持久卷申请和持久卷的StorageClass需要匹配，这使它没有接口灵活。后面会详细讲解。

- 动态持久卷：

在这种情况下，你只需创建持久卷申请（不需要单独创建持久卷），然后把持久卷申请与部署绑定。系统会按照持久卷申请自动创建持久卷。下面是持久卷申请配置文件。其中“storage：1Gi”，是指申请的空间大小是1G。

- 创建 持久卷申请（PersistentVolumeClaim）

```
kubectl apply -f k8s/mysql/mysql-volume.yaml
```

- 查看 持久卷申请（PersistentVolumeClaim）

```
kubectl get pvc
```

- 查看 持久卷申请（PersistentVolumeClaim）详细信息

```
kubectl describe pvc mysql-pv-claim
```

- 显示 持久卷(PersistentVolume)

```
kubectl get pv
```

- 显示 持久卷(PersistentVolume) 详细信息

```
kubectl describe pv pvc-ac6c88d5-ef5a-4a5c-b499-59715a2d60fa
```

- 查看 MySQL 目录信息：

```
/tmp/hostpath-provisioner/pvc-ac6c88d5-ef5a-4a5c-b499-59715a2d60fa$ ls -al
```

- 持久卷的回收模式：

当持久卷和持久卷申请被删除后，它有三种回收模式。

  1. ** 保持（Retain）**：当持久卷申请被删除后，持久卷仍在。你可以手动回收持久卷里的数据。
  2. ** 删除（Delete）**：持久卷申请和持久卷都被删除，底层存储的数据也会被删除。当使用动态持久卷时，缺省的模式是Delete。当然，你可以在持久卷被创建之后修改它的回收模式。
  3. ** 回收（Recycle）**：这种方式已经不推荐使用了，建议用Retain代替

- 静态持久卷：

动态持久卷的一个问题是它的缺省回收模式是“删除”，这样当虚机重新启动后，持久卷会被删除。当你重新运行部署时，k8s会创建一个新的MySQL，这样原来MySQL里的新建信息就会丢失，这是我们不愿意看到的。虽然你可以手动修改回收方式为“保持”，但还是要手动回收原来持久卷里的数据。
一个解决办法是把持久卷建在宿主机上，这样即使虚机出了问题被重新启动，MySQL里的新建信息依然不会丢失。如果是在云上，就会有专门的的存储层，如果是本地，大致有三种方式：

1. Local：把存储从宿主机挂载到k8s集群上. 详情请参见："[Volumes](https://kubernetes.io/docs/concepts/storage/volumes/#local)".
2. HostPath：也是把存储从宿主机挂载到 k8s 集群上，但它有许多限制，例如只支持单节点（Node），而且只支持“ReadWriteOnce”模式。详情请参见： "[hostPath as volume in kubernetes](https://stackoverflow.com/questions/50001403/hostpath-as-volume-in-kubernetes)".
3. NFS：网络文件系统，这种是最灵活的，但需要安装NFS服务器。详情请参见："[Kubernetes Volumes Guide](https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-volumes-example-nfs-persistent-volume.html)".

选择了比较简单的“Local”方式的话，必须单独创建持久卷，不能 只创建持久卷申请而让系统自动创建持久卷，见 mysql-volume-local.yaml。

- 查看是否安装了缺省的 storageClass 

```
kubectl get sc
```

- 查看缺省的 storageClass 详细信息

```
kubectl describe sc

```

- 查看已创建好的 configMap

```
kubectl get configMap
```

- 查看 configMap 的详细信息

```
kubectl describe configMap
```

- 查看 secret mysql-secret 的详细信息

```
kubectl describe secret mysql-secret
```

- Environment Variable：

环境变量一般是在部署里面定义的，没有单独的配置文件。下面是部署配置文件里的环境变量的片段。“MYSQL_ROOT_PASSWORD”是环境变量名，“secretKeyRef”说明它的值来自于secret，“name: mysql-secret”是secret的名字，“key: mysql-user-root-pwd”是secret里的键名，它的最终含义就是环境变量“MYSQL_ROOT_PASSWORD”的值是由“mysql-user-root-pwd”来定义，而“mysql-user-root-pwd”是secret里面的一个键。

```
 env:
     - name: MYSQL_ROOT_PASSWORD
       valueFrom:
          secretKeyRef:
            name: mysql-secret
            key: mysql-user-root-pwd
```

引用了 configMap 和 secret 的 deployment 文件见 mysql-config-deployment.yaml

## 下一步

- Helm 
- Terraform

