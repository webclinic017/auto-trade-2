# Heptio Velero

https://katacoda.com/courses/kubernetes/heptio-velero

## Set Up our Environment

```bash
git clone https://github.com/heptio/velero

curl -LO https://github.com/heptio/velero/releases/download/v1.1.0/velero-v1.1.0-linux-amd64.tar.gz

tar -C /usr/local/bin -xzvf velero-v1.1.0-linux-amd64.tar.gz

export PATH=$PATH:/usr/local/bin/velero-v1.1.0-linux-amd64/

echo "[default]
aws_access_key_id = minio
aws_secret_access_key = minio123" > credentials-velero

kubectl apply -f velero/examples/minio/00-minio-deployment.yaml

velero install \
    --provider aws \
    --bucket velero \
    --secret-file ./credentials-velero \
    --use-volume-snapshots=false \
    --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.velero.svc:9000

kubectl apply -f velero/examples/nginx-app/base.yaml

kubectl get deployments -l component=velero --namespace=velero

kubectl get deployments --namespace=nginx-example
```

## Back Up Our Resources

```bash
velero backup create nginx-backup --selector app=nginx

velero backup describe nginx-backup

# Now, let's simulate a disaster:
kubectl delete namespace nginx-example
# NOTE: You might need to wait for a few minutes for the namespace to be fully cleaned up.

# Check that the nginx service and deployment are gone:
kubectl get deployments --namespace=nginx-example
kubectl get services --namespace=nginx-example
kubectl get namespace/nginx-example

# You should get no results.
```

## Restore Our Resources

```bash
velero restore create --from-backup nginx-backup
velero restore get
# If there are errors or warnings, you can look at them in detail:
# velero restore describe <RESTORE_NAME>

# You can verify that the nginx resources are available again:
kubectl get services --namespace=nginx-example
kubectl get namespace/nginx-example

```