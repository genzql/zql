#
FROM python:3.12
#
RUN pip install poetry==1.7.1

WORKDIR /code
COPY . /code
RUN poetry install --no-dev

#
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]