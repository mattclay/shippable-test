#!/bin/bash

set -ux

virtualenv --python /usr/bin/python3.7 ~/.test-venv
~/.test-venv/bin/python --version
~/.test-venv/bin/pip --version
