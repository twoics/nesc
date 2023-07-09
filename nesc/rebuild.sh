#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
cd "$parent_path" || exit

python nesc/setup.py sdist
python nesc/setup.py bdist_wheel

ls -a
ls nesc/

twine check dist/*
