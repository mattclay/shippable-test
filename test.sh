#!/bin/bash -eux

apt-get install shellcheck
shellcheck test.sh
