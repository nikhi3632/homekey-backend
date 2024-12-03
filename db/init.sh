#!/bin/bash
set -e
chmod +x /docker-entrypoint-initdb.d/init.sh
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    \i /docker-entrypoint-initdb.d/migrations/01_create_schema.sql
    \i /docker-entrypoint-initdb.d/seeds/01_seed_data.sql
EOSQL
