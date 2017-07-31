#!/bin/bash

if [ "${TEST}" = "1" ]; then
    ip addr show

    which python
    python -V

    which python2
    python2 -V

    which python2.6
    python2.6 -V

    which python2.7
    python2.7 -V

    which python3
    python3 -V

    which python3.5
    python3.5 -V

    which python3.6
    python3.6 -V

    env

    pip install pyyaml

    python -c 'import yaml; print(yaml.__version__);'
elif [ "${TEST}" = "2" ]; then
    echo "2: failing"
    exit 1
elif [ "${TEST}" = "3" ]; then
    echo "3: passing"
    exit 0
else
    echo "unknown: failing"
    exit 1
fi