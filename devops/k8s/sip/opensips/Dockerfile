FROM debian:11.1
RUN apt-get update -y
# 编译安装opensips，所需要依赖环境
RUN apt-get install -y sngrep vim wget gcc bison flex make openssl unixodbc libxml2 libncurses5-dev gnupg2 less libsctp* libmysqlclient* zlib* libpq* libmicrohttpd* libjson-c-dev libmongoc-dev default-libmysqlclient-dev mariadb-server libhiredis* libxml2* libpcre*
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 049AD65B
RUN echo "deb https://apt.opensips.org bullseye cli-nightly" >/etc/apt/sources.list.d/opensips-cli.list
# 安装opensips-cli工具
RUN apt-get update -y && apt-get install -y opensips-cli
# 把opensips 3.2.3源码文件夹添加到镜像里，注意：opensips-3.2.3文件夹需要跟Dockerfile文件是同一层目录
RUN mkdir -p /tools/software/opensips-3.2.3
ADD ./opensips-3.2.3 /tools/software/opensips-3.2.3
# include_modules 选择需要的模块进行编译安装
RUN cd /tools/software/opensips-3.2.3 && make all include_modules="db_mysql db_postgres proto_tls proto_wss tls_mgm cachedb_mongodb cachedb_redis httpd json xcap presence presence_xml dialplan" prefix="/usr/local/opensips" install
# 添加 opensips.cfg 配置文件
RUN mkdir -p /usr/local/etc/opensips/
RUN cp /usr/local/opensips/etc/opensips/opensips.cfg /usr/local/etc/opensips/opensips.cfg

VOLUME ["/usr/local/opensips/etc"]
VOLUME ["/usr/local/etc/opensips/"]
EXPOSE 5060/udp
ENTRYPOINT ["/usr/local/opensips/sbin/opensips", "-FE"]
