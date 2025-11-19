#!/bin/bash
# PostgreSQL Backup Script for Airflow Database
# This script creates timestamped backups of the PostgreSQL database

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/airflow_backup_${TIMESTAMP}.sql.gz"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-7}

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

echo "Starting PostgreSQL backup at $(date)"
echo "Backup file: ${BACKUP_FILE}"

# Create backup using docker exec
docker exec airflow-metabase-1 pg_dump \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    --format=plain \
    --no-owner \
    --no-acl \
    | gzip > "${BACKUP_FILE}"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully!"
    echo "Backup size: $(du -h "${BACKUP_FILE}" | cut -f1)"

    # Remove old backups older than retention period
    echo "Cleaning up backups older than ${RETENTION_DAYS} days..."
    find "${BACKUP_DIR}" -name "airflow_backup_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete

    echo "Backup process completed at $(date)"
else
    echo "ERROR: Backup failed!" >&2
    exit 1
fi
