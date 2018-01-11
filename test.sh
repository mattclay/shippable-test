#!/bin/bash -eux

env
uname -a
dmesg

cat /sys/kernel/debug/x86/pti_enabled
cat /sys/kernel/debug/x86/ibpb_enabled
cat /sys/kernel/debug/x86/ibrs_enabled
