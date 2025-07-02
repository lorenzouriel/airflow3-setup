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

# Install ODBC driver 17 for SQL Server
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Change to airflow user for subsequent commands
USER airflow

# Copy the requirements file
# This file should be in the same directory as the Dockerfile
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt --verbose

USER airflow