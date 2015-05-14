#!/bin/sh

./build.sh
cd BIN
CFLAGS=-g make bitmap
cd ..
./clear.sh
./main.py
