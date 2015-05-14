#!/bin/sh

find MUT -name "*" -exec rm -f {} \; &> /dev/null
find . -name "*.pyc" -exec rm -f {} \; &> /dev/null
find . -name "*.o" -exec rm -f {} \; &> /dev/null
