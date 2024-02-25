#
FROM python:3.12-slim
#
RUN pip install poetry==1.7.1

WORKDIR /code
COPY . /code
RUN poetry install --no-dev