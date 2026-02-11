### Docker start

Start everything with:
`docker compose up --build`

This starts:
- `server` (FastAPI on `http://localhost:8000`)
- `postgres`
- `redis`
- `sass` (watches SCSS and writes CSS)

### SCSS / CSS workflow

The `sass` service watches and compiles:
- `app/static/css/main.scss` -> `app/static/css/style.css`
- `app/static/css/results.scss` -> `app/static/css/results.css`

So when you change SCSS files locally, CSS is rebuilt automatically while Compose is running.

### Image build behavior

The `Dockerfile` also compiles SCSS in a dedicated Node build stage and copies:
- `style.css`
- `results.css`

into the final Python image.  
This makes the image reproducible even without running the `sass` watcher.

### References
- [Docker Python guide](https://docs.docker.com/language/python/)
