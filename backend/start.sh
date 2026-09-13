#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"
exec ./env/Scripts/python.exe -m uvicorn main:app --reload --port 8000