# k8s & Mongo

## docker & mongo

```bash
# 8.8 mongodb

mkdir -p ~/apps/mongodb/data ~/apps/mongodb/backup
docker pull mongo:4.2


# --restart=always \
# --privileged=true \
docker run -d \
--name mongo \
-p 27018:27017 \
-v ~/apps/mongodb/data:/data/db \
-v ~/apps/mongodb/backup:/data/backup \
mongo:4.2 --auth

docker exec -it mongo mongo admin
    db.createUser({ user: 'admin', pwd: '123456', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
    db.auth("admin","123456");

docker exec mongo sh -c 'exec var=`date +%Y%m%d%H%M` && mongodump -h localhost --port 27017 -u jsmith -p password -d dbname -o /data/backup/$var_test1.dat'
```