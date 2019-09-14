#!/bin/bash
export PGPASSWORD=$DB_PASS
psql -U $DB_USER -c "drop database ${DB_NAME}"
