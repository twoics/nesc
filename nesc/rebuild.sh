#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
cd "$parent_path" || exit

ls ls nesc/ -a
#rm -rf build/
#rm -rf dist/
#rm -rf serializer_service.egg-info/
#
#python setup.py sdist
#python setup.py bdist_wheel
#
#twine check dist/*
