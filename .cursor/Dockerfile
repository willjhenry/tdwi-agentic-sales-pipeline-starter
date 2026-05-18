# syntax=docker/dockerfile:1
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6 libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ubuntu

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER ubuntu
WORKDIR /home/ubuntu

# Cursor mounts the cloned workspace at runtime — no COPY of application code
