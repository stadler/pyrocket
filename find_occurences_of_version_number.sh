#!/bin/bash

grep -Ir --exclude-dir=.svn --exclude=*.svg --exclude=*.changes --exclude=*.build --exclude=*.dsc "0\.7" *
