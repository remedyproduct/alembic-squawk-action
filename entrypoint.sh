#!/usr/bin/env bash
set -e

echo "Running entrypoint in Docker container..."

# The changed migrations files (passed via environment or arguments)
MIGRATIONS_FILES="$INPUT_MIGRATIONS_FILES"

if [ -z "$MIGRATIONS_FILES" ]; then
  echo "No new migrations found."
  echo "changed=false" >> "$GITHUB_OUTPUT"
  exit 0
fi

echo "Found changed migrations: $MIGRATIONS_FILES"

# Generate the Alembic revision range
ALEMBIC_RANGE=$(poetry run python /app/scripts/range_from_files.py -f "$MIGRATIONS_FILES")

echo "Alembic range: $ALEMBIC_RANGE"

# Generate SQL
poetry run alembic upgrade "$ALEMBIC_RANGE" --sql > /github/workspace/migrations.sql

echo "changed=true" >> "$GITHUB_OUTPUT"
