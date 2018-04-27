#!/bin/bash

while :
do
    clear
    ./test.py
    inotifywait -e close_write *.py
done
