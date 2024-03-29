#!/bin/bash

PROJECT_HEAD_DIR="$(pwd)/${0%/*}/.."
cd ${PROJECT_HEAD_DIR}

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pygame
python3 src/Main.py
