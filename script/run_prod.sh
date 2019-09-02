#!/usr/bin/env bash
source ./env/bin/activate
source ./script/prod.sh
make prod
python -m app.app
