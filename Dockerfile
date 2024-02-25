#
FROM python:3.12-slim

# install deps
RUN pip install poetry==1.7.1

WORKDIR /code
COPY pyproject.toml /code
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


COPY . /code
ENTRYPOINT ["uvicorn",  "main:app"]
CMD ["--host", "0.0.0.0", "--port", "80", "--reload"]