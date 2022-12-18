## This is a demo that demonstrates KEDA with a python consumer for a RabbitMQ queue

### Prerequisites

1. deploy KEDA Operator
2. pip install pika
3. if running on minikube, make sure that pod metrics are available (metrics-server addon)

First, we'll create the RabbitMQ instance and port-forward to it

    helm repo add my-repo https://charts.bitnami.com/bitnami
    helm install rabbitmq bitnami/rabbitmq -n rabbitmq --set auth.user=user,auth.password=password,podSecurityContext.enabled=false,containerSecurityContext.enabled=false --create-namespace
    kubectl port-forward --namespace rabbitmq svc/rabbitmq 5672:5672 &
    kubectl port-forward --namespace rabbitmq svc/rabbitmq 15672:15672 &

Then, we'll deploy our consumer

    kubectl apply -f deployment.yaml

We'll first create a HorizontalPodAutoscaler and see the time it takes for our application to scale up and down, until the queue is cleared

    kubectl apply -f hpa.yaml
    python src/producer/app.py

Then, we'll delete that HPA and create KEDA's ScaledObject and see how it comares

    kubectl delete -f hpa.yaml
    kubectl apply -f scaledobject.yaml
    python src/producer/app.py

You can run the producer serveral times to see the queue build up and the pod replica changes 
