# zql

SQL for Gen Z.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/genzql/zql)

## Getting Started

1. Install poetry and Docker.
2. Run application: `docker compose up`
3. Run tests: `docker compose -f test-docker-compose.yml up --build`

## Commands

Start a shell inside the container:

```bash
docker exec -it zql_web bash
```

Run unit tests:

```bash
poetry run pytest
```

## Releases

Currently, we manually release new versions of the [`genzql`](https://pypi.org/project/genzql/) package to PyPI.

Vinesh Kannan (vingkan@gmail.com) is the current release manager.

```bash
cd zql
poetry build
poetry publish --username __token__ --password pypi-token...
```
