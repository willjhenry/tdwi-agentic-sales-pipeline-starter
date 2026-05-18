# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Cloud Agent interactive terminals attach via tmux (see Cursor cloud agent docs).
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    git \
    sudo \
    tmux \
    libfreetype6 \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Cloud Agents expect a login user named ubuntu for shell/terminal access.
RUN useradd -m -s /bin/bash ubuntu && \
    echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu

# Install Python deps as root before switching user (avoids pip permission errors).
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER ubuntu
WORKDIR /home/ubuntu

# Cursor mounts the cloned workspace at runtime — no COPY of application code
