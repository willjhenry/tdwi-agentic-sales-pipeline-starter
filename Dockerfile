# syntax=docker/dockerfile:1
# Full image (not slim): more system libs/build tools; still add Cloud Agent essentials below.
FROM python:3.12

# tmux/sudo/git are not in the official Python image; required for Cloud Agent terminals.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    sudo \
    tmux \
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
