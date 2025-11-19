#!/bin/bash
# PostgreSQL Restore Script for Airflow Database
# Usage: ./restore-db.sh <backup_file>

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh ./backups/airflow_backup_*.sql.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "ERROR: Backup file '${BACKUP_FILE}' not found!" >&2
    exit 1
fi

echo "WARNING: This will restore the database from backup: ${BACKUP_FILE}"
echo "Current database '${POSTGRES_DB}' will be dropped and recreated!"
read -p "Are you sure you want to continue? (yes/no): " -r
echo

if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Restore cancelled."
    exit 0
fi

echo "Starting PostgreSQL restore at $(date)"
echo "Restore file: ${BACKUP_FILE}"

# Stop Airflow services (except postgres)
echo "Stopping Airflow services..."
docker compose stop airflow-apiserver airflow-scheduler airflow-dag-processor airflow-triggerer airflow-worker

# Drop and recreate database
echo "Recreating database..."
docker exec airflow-metabase-1 psql -U "${POSTGRES_USER}" -c "DROP DATABASE IF EXISTS ${POSTGRES_DB};"
docker exec airflow-metabase-1 psql -U "${POSTGRES_USER}" -c "CREATE DATABASE ${POSTGRES_DB};"

# Restore from backup
echo "Restoring from backup..."
gunzip -c "${BACKUP_FILE}" | docker exec -i airflow-metabase-1 psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"

if [ $? -eq 0 ]; then
    echo "Restore completed successfully!"

    # Restart Airflow services
    echo "Restarting Airflow services..."
    docker compose up -d airflow-apiserver airflow-scheduler airflow-dag-processor airflow-triggerer airflow-worker

    echo "Restore process completed at $(date)"
else
    echo "ERROR: Restore failed!" >&2
    exit 1
fi
