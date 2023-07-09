#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

rm -rf build/
rm -rf dist/
rm -rf serializer_service.egg-info/

python setup.py sdist
python setup.py bdist_wheel

twine check dist/*
