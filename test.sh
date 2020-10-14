#!/bin/bash

env

ls -l ~/.ansible-core-ci-private.key

docker ps

set -eux

cat /proc/self/cgroup
cat /proc/self/cpuset
cat /proc/self/mountinfo
