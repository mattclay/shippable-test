#!/bin/bash

add-apt-repository ppa:fkrull/deadsnakes && apt-get update -qq && apt-get install python2.4 -qq

python    -V
python2.4 -V
python2.6 -V
python2.7 -V
python3.5 -V
