# Image: Apache Airflow with Python dependencies
# This Dockerfile builds an Apache Airflow image with additional Python dependencies.
FROM apache/airflow:3.0.0

# Install dependencies for building Python packages
# Use the root user to install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Change to airflow user for subsequent commands
USER airflow

# Copy the requirements file
# This file should be in the same directory as the Dockerfile
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt --verbose

USER airflow