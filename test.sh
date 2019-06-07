#!/bin/bash

set -ux

command -V python
python --version

command -V pip
pip --version

python -m pip --version

command -V python3.7
python3.7 --version

command -V pip3.7
pip3.7 --version

python3.7 -m pip --version
