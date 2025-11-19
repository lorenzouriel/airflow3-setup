# Image: Apache Airflow with Python dependencies
# This Dockerfile builds an Apache Airflow image with additional Python dependencies.
FROM apache/airflow:3.1.3

# Install all system dependencies in a single layer
USER root

# Combine all apt-get operations into a single RUN command to reduce layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build dependencies for Python packages
    build-essential \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    git \
 && apt-get update \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Switch to airflow user for Python package installation
USER airflow

# Copy requirements file
COPY requirements.txt /requirements.txt

# Install Python dependencies in a single layer
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt

# Ensure we're running as airflow user
USER airflow