#!/bin/bash

add-apt-repository ppa:fkrull/deadsnakes && apt-get update -qq && apt-get install python2.4 -qq

python    --version
python2.4 --version
python2.6 --version
python2.7 --version
python3.5 --version
