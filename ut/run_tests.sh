#!/bin/sh

cd ..
pip3 install -r conf/requirements.txt
if ! flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    exit 1
fi
if ! flake8 . --count --max-complexity=10 --max-line-length=127 --statistics; then
    exit 1
fi
if [ "$1" = "full" ]; then
pytest --cov-config=ut/.coveragerc --cov . --cov-fail-under=85 -v
else
pytest . -k "not test_getters_gecko_interface" -vrP
fi
