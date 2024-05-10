FROM tiangolo/uvicorn-gunicorn:python3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y redis-server

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY app /app