#!/usr/bin/env bash
source ./env/bin/activate
source ./script/dev.sh
make dev
python -m app.app
