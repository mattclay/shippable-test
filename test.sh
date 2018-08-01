#!/bin/bash -x

curl --silent https://bootstrap.pypa.io/get-pip.py | python3.6
pip3.6 install cryptography requests
