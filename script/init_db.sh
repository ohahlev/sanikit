#!/bin/bash
export PGPASSWORD=$DB_PASS
psql -U $DB_USER -c "create database ${DB_NAME}"