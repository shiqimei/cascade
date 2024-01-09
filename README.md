# Cascade

A GitHub App designed to streamline your workflow through seamless authorization and integration.

## Local Development

```bash
poetry install
poetry run dev
poetry run gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:8080 src.app:app

```

## Production Deployment

```bash
docker build -t cascade .
docker run -p 8080:80 cascade
```

Keep secrets secure

```bash
kubectl create namespace cascade-chat
poetry run buildpoetry run build_secret_yaml && kubectl apply -f deployment-secret.yaml
```

#### Notes

1. **For VSCode Users:** Make sure correct python interpreter is selected with `Python: Select Interpreter`.
2. Generate a new `JWT_SECRET_KEY` or `GITHUB_WEBHOOK_SECRET`, use command `poetry run secret`
3. Reverse proxy local port for testing: [pinggy.io](https://pinggy.io/)