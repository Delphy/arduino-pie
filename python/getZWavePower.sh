#!/bin/sh

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR

python getZWavePower.py
