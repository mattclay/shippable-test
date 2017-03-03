#!/bin/bash -eux

add-apt-repository 'deb http://archive.ubuntu.com/ubuntu trusty-backports universe'
add-apt-repository 'ppa:fkrull/deadsnakes'
apt-get update -qq
apt-get install python2.4 shellcheck -qq

pip install coverage

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

cp sample.json shippable/testresults/not-a-test.json
