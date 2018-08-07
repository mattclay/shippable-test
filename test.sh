#!/bin/bash -x

openssl ecparam -name secp384r1 -genkey -noout

curl --silent https://bootstrap.pypa.io/get-pip.py | python3.6
pip3.6 install cryptography requests
./test.py
