# GitHub App Demo

## Local Development

```bash
poetry install
poetry run dev
poetry run gunicorn -b 0.0.0.0:8080 src.app:app
```

## Production Deployment

```bash
docker build -t github-app-demo .
docker run -p 8080:80 github-app-demo
```

#### Notes

**For VSCode Users:** Make sure correct python interpreter is selected with `Python: Select Interpreter`.