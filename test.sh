#!/bin/bash -eux

env
apt-get install attr

getfattr /dev/null
