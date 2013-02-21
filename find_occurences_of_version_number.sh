#!/bin/bash
EXPECTED_ARGS=1
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` {VERSION_NUMBER}"
  exit 1
fi
grep -Ir --exclude-dir=.svn --exclude=*.svg --exclude=*.changes --exclude=*.build --exclude=*.dsc "$1" *
