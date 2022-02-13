# syntax=docker/dockerfile:1
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR app
COPY . /app/
RUN pip install -r requirements.txt  && \
    ln -s /app/share /share