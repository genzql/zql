#
FROM python:3.12-slim
#
RUN pip install poetry==1.7.1

WORKDIR /code
COPY . /code
RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "uvicorn",  "main:app"]
CMD ["--host", "0.0.0.0", "--port", "80", "--reload"]