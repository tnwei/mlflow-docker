FROM python:3.9-slim-bullseye
# psycopg2 deps
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install mlflow boto3 psycopg2
