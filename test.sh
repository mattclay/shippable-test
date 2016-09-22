#!/bin/bash -eux

apt-add-repository 'deb http://archive.ubuntu.com/ubuntu trusty-backports universe'
apt-get update -qq
apt-get install shellcheck
shellcheck test.sh
