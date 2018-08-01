#!/bin/bash -x

env

curl https://bootstrap.pypa.io/get-pip.py | python3.6

which pip
which pip3.6

pip list
pip3.6 list

python -m pip list
python3.6 -m pip list
