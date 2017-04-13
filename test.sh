#!/bin/bash

ls -l /usr/bin/python*
ls -l /usr/local/bin/python*
ln -s /usr/bin/python3.5 /usr/local/bin/python
ls -l /usr/local/bin/python*

which python
python -V

which python2
python2 -V

which python2.6
python2.6 -V

which python2.7
python2.7 -V

which python3
python3 -V

which python3.5
python3.5 -V

which python3.6
python3.6 -V

env
