# freeswitch

## build image

```bash
docker build . -t buster_freeswitch_1.10.7:1.0 -f Dockerfile

# 查看镜像
docker images | grep freeswitch
```

## run image

```bash
# 运行镜像
docker run \
    --name=buster_freeswitch_1.10.7 \
    --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/freeswitch/bin \
    --volume=/data:/data \
    --network=host \
    -itd \
    buster_freeswitch_1.10.7:1.0

# 查看容器运行状态
docker ps | grep freeswitch
# 进入容器（需替换 container_id）
docker exec -it ${container_id} bash
```

## config

```bash
vim /usr/local/freeswitch/conf/vars.xml
# 修改默认密码 default_password 如 123456
# 如果需要外网可访问注册到电话系统 修改 domain=外网ip
# 基本配置完成，启动 FreeSwitch 
# 先前台运行看看（后台运行命令 freeswitch -nc 可以 fs_cli 进入交互窗口）
freeswitch 
# 成功运行，用 microsip 注册一个话机试试（xlite、linphone、microsip 等软件均可）

```