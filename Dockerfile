# syntax=docker/dockerfile:1
# ================================================
# TDWI Lab 3 – Cloud Agent Dockerfile
# See: https://cursor.com/environment-json-dockerfile.md
# ================================================

# Full Python image (not slim) — includes more system libs for builds and matplotlib.
FROM python:3.13

# Cloud Agent terminals run in tmux (see Cursor cloud agent setup docs).
# git/sudo are commonly needed for repo work and passwordless admin tasks.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    sudo \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Good practice per environment-json-dockerfile.md: non-root user "ubuntu" with a home dir,
# matching "user": "ubuntu" in .cursor/environment.json.
RUN useradd -m -s /bin/bash ubuntu && \
    echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu

# Install Python dependencies as root before switching user (avoids pip permission errors).
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Default user/home for shells (good practice per environment-json-dockerfile.md).
# WORKDIR does not set where the install script runs or where agents work — Cursor runs
# install from the project root and mounts the cloned repo as the workspace.
USER ubuntu
WORKDIR /home/ubuntu

# No COPY of application code — Cursor mounts the cloned workspace at runtime.
