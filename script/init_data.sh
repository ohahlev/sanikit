#!/bin/bash
export PGPASSWORD=$DB_PASS
psql -U $DB_USER -d $DB_NAME -a -f schema.sql