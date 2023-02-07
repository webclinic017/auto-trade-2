# K8S & clickhouse

## v1 

1. 创建一个 docker-compose.yml 文件：

```yaml
version: '3'
services:
  clickhouse:
    image: yandex/clickhouse-server
    ports:
      - "8123:8123"
```

2. 运行以下命令：

```bash
docker-compose up
```

3. 检查容器运行状态：

```bash
docker-compose ps
```

4. 连接到容器并进入 ClickHouse 控制台：

```bash
docker-compose exec clickhouse clickhouse-client
```

在控制台中，您可以使用 SQL 语句进行操作，例如创建数据库、表等。

这是在 Docker Compose 中安装 ClickHouse 的一个简单示例，
它只是 Docker Compose 的基本用法，您可以通过深入了解 Docker Compose 和 ClickHouse 的文档，
以获得更多详细的信息。



