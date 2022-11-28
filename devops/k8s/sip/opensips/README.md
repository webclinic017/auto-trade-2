# opensips

## build image

```bash
docker build -t opensips-3.2.3 .

# 查看镜像
docker images | grep opensips
```

## run image

```bash
# 运行镜像
# 宿主机目录：/data/opensips，需要提前准备opensips.cfg配置文件。
docker run --name opensips -it -v /data/opensips:/usr/local/opensips/etc/opensips -d opensips-3.2.3

# 查看容器运行状态
docker ps | grep opensips
# 进入容器（需替换 container_id）
docker exec -it ${container_id} bash
```

## config

```bash
# 进入容器
docker exec -it opensips bash
# 新增.opensips-cli.cfg配置
vim ~/.opensips-cli.cfg

```

以下为.opensips-cli.cfg配置

```
[default]
log_level: WARNING
prompt_name: opensips-cli
prompt_intro: Welcome to OpenSIPS Command Line Interface!
prompt_emptyline_repeat_cmd: False
history_file: ~/.opensips-cli.history
history_file_size: 1000
output_type: pretty-print
communication_type: fifo
fifo_file: /tmp/opensips_fifo

# 选择模块添加数据库表结构
database_modules: ALL

# 数据库脚本目录
database_schema_path: /usr/local/opensips/share/opensips

# 数据库管理员账号
#database_admin_url: postgres://root@localhost
database_admin_url: mysql://root@localhost

# 会新建数据库账号：opensips，密码：opensipsrw
# database_url: postgres://opensips:opensipsrw@localhost
database_url: mysql://opensips:opensipsrw@localhost
# 数据库名称
database_name: opensips
```


保存.opensips-cli.cfg配置内容，后执行
```bash
opensips-cli -x database create
# 执行后需输入数据库管理员账号的密码
# 没有报错即可退出容器
exit
```