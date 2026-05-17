# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for matplotlib on slim image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# <-- This is the important security pattern for Module 4 -->
RUN --mount=type=secret,id=REPORT_EXPORT_KEY \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create directories the agent will need
RUN mkdir -p data output

# Default command (the agent will override this as needed)
CMD ["python", "src/generate_sales_report.py"]