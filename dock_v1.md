# Documentation

## config-2023mt0361.yaml

This file defines a Kubernetes ConfigMap for the FastAPI application.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-2023mt0361
data:
  APP_VERSION: "1.0"
  APP_TITLE: "My FastAPI App"
```

## deployment.yaml

This file defines a Kubernetes Deployment for the FastAPI application.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi-container
          image: img-2023mt0361-app:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: config-2023mt0361
```

## main.py

This file contains the main FastAPI application code.

```python
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from prometheus_fastapi_instrumentator import Instrumentator

# Explicitly load .env file
load_dotenv(override=True)

# Create the FastAPI application
app = FastAPI()

# Add Instrumentator middleware and expose metrics at `/metrics`
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)
instrumentator.instrument(app)

@app.get("/get_info")
def get_info():
    app_version = os.getenv("APP_VERSION", "default_version")
    app_title = os.getenv("APP_TITLE", "default_title")
    return {"app_version": app_version, "app_title": app_title}

# Use the `startup` lifecycle event with a dedicated function
@app.on_event("startup")
async def startup_event():
    print("Application has started From Main File")
```

## prometheus-config.yaml

This file defines a Kubernetes ConfigMap for Prometheus configuration.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'fastapi'
        static_configs:
          - targets: 
            - 'fastapi-service:80'
```

## prometheus-deployment.yaml

This file defines a Kubernetes Deployment for Prometheus.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  labels:
    app: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:latest
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: prometheus-config
              mountPath: /etc/prometheus/
              subPath: prometheus.yml
      volumes:
        - name: prometheus-config
          configMap:
            name: prometheus-config
```

## prometheus-service.yaml

This file defines a Kubernetes Service for Prometheus.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: prometheus
spec:
  type: NodePort
  selector:
    app: prometheus
  ports:
    - protocol: TCP
      port: 9090
      targetPort: 9090
      nodePort: 30000
```

## service.yaml

This file defines a Kubernetes Service for the FastAPI application.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  selector:
    app: fastapi
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```
