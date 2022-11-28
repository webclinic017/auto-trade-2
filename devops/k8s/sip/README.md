# SIP & Linphone

## opensips

sip 信令服务器
https://opensips.org/Downloads/Downloads

```bash
# 拉取镜像: 
# https://github.com/daxiondi/docker-opensips.git
# opensips/opensips:3.1 没有 opensipsctl
docker pull opensips/opensips:3.1      
# 创建容器运行: 
docker run -d -it \
--name sip \
-p 5060:5060/udp \
opensips/opensips:3.1
               
# 拷贝文件: 
docker cp opensips.cfg opensips:/etc/opensips/opensips.cfg

cp /etc/opensips/opensipsctlrc /etc/opensips/opensipsctlrc.backup
apt-get install mysql-client
docker cp opensips:/etc/opensips/opensipsctlrc .
docker cp opensipsctlrc opensips:/etc/opensips/opensipsctlrc


# 启动容器: 
docker start sip
# 停止容器: 
docker stop sip
# 重启容器: 
docker restart sip
# 删除容器: 
docker rm -f sip（容器名字 NAMES）

# 容器终端: 
docker exec -it sip /bin/bash

# 显示所有容器IP地址：
docker inspect --format='{{.Name}} - {{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq)

# 针对单个容器查看IP: docker inspect 容器ID | grep IPAddress
docker inspect sip | grep IPAddress

# 配置opensips.cfg 

# 1. 拷贝出文件: 
# docker cp sip:/etc/opensips/opensips.cfg .
# 2.修改opensips.cfg文件:

# 修改前
# /* comment the next line to enable the auto discovery of local aliases
#    based on reverse DNS on IPs */
# auto_aliases=no
 
# listen=udp:172.17.0.2:5060
 
 
# 修改后
# /* comment the next line to enable the auto discovery of local aliases
#    based on reverse DNS on IPs */
# auto_aliases=no
# //如果需要在公网下使用，这里可以配置公网ip，端口映射后亲测可用
# advertised_address="192.168.1.170"
# alias="192.168.1.170"
 
# listen=udp:172.17.0.2:5060


# 3.再拷贝进容器: 
# docker cp opensips.cfg sip:/etc/opensips/opensips.cfg
# 4.重启容器: 
# docker restart sip

# NAT
# 1. bridge 模式下配置
docker cp opensips:/etc/opensips/opensips.cfg .
vim opensips.cfg

# 找到 socket=udp:172.17.0.4:5060然后添加以下行
advertised_address="public ip:5060"

docker cp opensips.cfg opensips:/etc/opensips/opensips.cfg 
docke restart opensips

# 2. host 模式 
docker run -tid --net=host --name opensips opensips/opensips:3.1

# 查看日志
docker logs -f opensips
```

## 进入docker 容器添加 opensips-mysql-module 模块

```bash
apt-get update
apt-get -y install opensips-mysql-module
# apt-get -y install opensips-http-module

# vim /usr/local/etc/opensips/opensipsctlrc
# 解除DBENGIN=MySQL这句话的注释。

# 容器内安装 mysql 
apt-get install mysql-server mysql-client libmysqlclient-dev
```
## 添加 opensips user

```bash
docker cp .opensips-cli.cfg opensips:/root/.opensips-cli.cfg

# 容器
opensips-cli -f /root/.opensips-cli.cfg
# 如果存在数据库 先删掉数据库： drop database opensips;
opensips-cli -x database create opensips
opensips-cli -x user add 1001@192.168.0.135 1001
opensips-cli -x user add 1002@192.168.0.135 1002

select * from subscriber;

```

## /etc/opensips/opensips.cfg

```
docker cp opensips:/etc/opensips/opensips.cfg .

socket=udp:eth0:5060   # CUSTOMIZE ME
# socket=udp:192.168.0.135:5060   # CUSTOMIZE ME
advertised_address="192.168.0.135:5060"

docker cp opensips.cfg opensips:/etc/opensips/opensips.cfg 
```

## Linphone 



