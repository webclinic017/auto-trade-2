# K8S & nginx

## Create Deployment

```
cat deployment.yaml
kubectl apply -f deployment.yaml
kubectl get deployment

```

## Deploy Ingress

```bash
cat ingress.yaml

kubectl create -f ingress.yaml

kubectl get deployment -n nginx-ingress
```

## Deploy Ingress Rules

```bash
cat ingress-rules.yaml
kubectl create -f ingress-rules.yaml
kubectl get ing
```

## Test

```bash
curl -H "Host: my.kubernetes.example" 172.17.0.19/webapp1

curl -H "Host: my.kubernetes.example" 172.17.0.19/webapp2

curl -H "Host: my.kubernetes.example" 172.17.0.19
```