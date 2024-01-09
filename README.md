# Cascade

A GitHub App designed to streamline your workflow through seamless authorization and integration.

## Local Development

```bash
poetry install
poetry run dev
poetry run gunicorn -b 0.0.0.0:8080 src.app:app
```

## Production Deployment

```bash
docker build -t cascade .
docker run -p 8080:80 cascade
```

#### Notes

**For VSCode Users:** Make sure correct python interpreter is selected with `Python: Select Interpreter`.