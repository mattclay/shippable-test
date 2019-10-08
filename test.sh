#!/bin/bash

set -ux

python -m pip --version
python -m pip list

python2.7 -m pip --version
python2.7 -m pip list

python3.5 -m pip --version
python3.5 -m pip list

python3.7 -m pip --version
python3.7 -m pip list
