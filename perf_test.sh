#!/bin/bash

echo "This script destroys files. Remove these two lines to run the test."
exit 1

dirpath="/tmp/fdated_perf"
echo "Recreate dir $dirpath (could take a couple of secs)"
rm -fr $dirpath
mkdir $dirpath

echo "Generate the test files (takes a few secs)"
# Work around argument list length restrictions
for each in {1800..1999}
do
    touch $dirpath/main_$each-{01..12}-{01..28}.log
done
echo "Find 4 files among `ls $dirpath | wc -l`"
time ./fdated.py -n 100 -o 95 -t 2000-01-01 $dirpath >/dev/null
