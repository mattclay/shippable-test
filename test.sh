#!/bin/bash

set -ux

python -m pip list
python3 -m pip list

openssl version
openssl ecparam -list_curves
