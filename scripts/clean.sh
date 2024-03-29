#!/bin/bash

PROJECT_HEAD_DIR="$(pwd)/${0%/*}/.."
cd ${PROJECT_HEAD_DIR}

rm -rf .venv
rm -rf src/__pycache__