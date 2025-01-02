#! /usr/bin/env sh

echo "Building Python Environment";
poetry env use python3.9
poetry install --with=dev
poetry run python3 -m pip install --upgrade pip setuptools

echo "Initializing Git repository"
git init
git remote add origin https://github.com/JKhakpour/retrie.git
