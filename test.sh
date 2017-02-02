#!/bin/bash -eux

shippable_retry add-apt-repository 'deb http://archive.ubuntu.com/ubuntu trusty-backports universe'
shippable_retry add-apt-repository 'ppa:fkrull/deadsnakes'
shippable_retry apt-get update -qq
shippable_retry apt-get install python2.4 shellcheck -qq

shippable_retry pip install coverage

which pip
pip --version

which python
python    -V

which python2.4
python2.4 -V

which python2.6
python2.6 -V

which python2.7
python2.7 -V

which python3.5
python3.5 -V

which coverage
coverage --version

which shellcheck
shellcheck --version

env
pwd

find .
