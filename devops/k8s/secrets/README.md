# Use Kubernetes to manage Secrets

## Create Secrets

```bash
username=$(echo -n "admin" | base64)
password=$(echo -n "a62fjbd37942dcs" | base64)
```

```bash
echo "apiVersion: v1
kind: Secret
metadata:
  name: test-secret
type: Opaque
data:
  username: $username
  password: $password" >> secret.yaml
```

```bash
kubectl create -f secret.yaml

kubectl get secrets

kubectl exec -it secret-env-pod env | grep SECRET_

kubectl get pods
```

## Consume via Environment Variables

```bash
cat secret-env.yaml

kubectl create -f secret-env.yaml

kubectl exec -it secret-env-pod env | grep SECRET_

kubectl get pods
```

## Consume via Volumes

```bash
cat secret-pod.yaml

kubectl create -f secret-pod.yaml

kubectl exec -it secret-vol-pod ls /etc/secret-volume

kubectl exec -it secret-vol-pod cat /etc/secret-volume/username

kubectl exec -it secret-vol-pod cat /etc/secret-volume/password

```

