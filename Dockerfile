# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set working directory — Cursor will mount the workspace here automatically
WORKDIR /app

# Install system dependencies (needed for matplotlib)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy ONLY requirements.txt (this is still required for the build step)
COPY requirements.txt .

# <-- Production best-practice: build secret for any private credentials -->
RUN --mount=type=secret,id=REPORT_EXPORT_KEY \
    pip install --no-cache-dir -r requirements.txt

# Create directories the agent will need (data/ is already in the repo, output/ is for generated files)
RUN mkdir -p output

# No CMD or COPY . . — Cursor handles the runtime workspace mount