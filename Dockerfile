# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Ultra-minimal Dockerfile for Cursor Cloud Agent Lab 3 (debugging)
WORKDIR /app

# Install the exact packages we need in one clean layer
RUN pip install --no-cache-dir pandas matplotlib pytest

# Create the output directory the agent will use for the report chart
RUN mkdir -p output

# Cursor automatically mounts the workspace at runtime — no COPY needed