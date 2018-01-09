#!/bin/bash -eux

env
apt-get install attr

touch foo
getfattr foo
setfattr -n user.foo foo
getfattr foo
setfattr -x user.foo foo
getfattr foo
