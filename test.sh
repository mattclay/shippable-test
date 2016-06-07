#!/bin/sh

env

if [ "${SHIPPABLE}" = "true" ]; then
    echo "It appears this job is running on Shippable instead of Travis."
    if [ "${IS_PULL_REQUEST}" = "true" ]; then
        echo "Please rebase the branch used for this pull request."
    else
        echo "This branch needs to be updated to work with Shippable."
    fi
    exit 1
fi
