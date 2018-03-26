#!/bin/bash -eux

env
pwd
ls -l /
find /shippableci
find /home
find /data

aws configure list
