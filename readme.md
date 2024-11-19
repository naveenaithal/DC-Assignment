minikube image load img-2023mt0361-app
kubectl apply -f config-2023mt0361.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

kubectl delete deployment fastapi-deployment
kubectl apply -f deployment.yaml

kubectl delete service fastapi-service
kubectl apply -f service.yaml

minikube service fastapi-service --url

kubectl delete pod --all

venv\Scripts\activate
uvicorn main:app --reload

kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-service.yaml

kubectl port-forward svc/prometheus 9090:9090

<!-- Navigate to http://localhost:9090. -->
