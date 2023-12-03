#!/usr/bin/env bash

echo "This script destroys files. Remove these two lines to run the test."
exit 1

check_dependency() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "Command $1 required, quitting" >&2
        exit 1
    }
}
for each in hyperfine find ; do
    check_dependency "$each"
done

dirpath="/tmp/fdated_perf"
echo "Recreate dir $dirpath (could take a couple of secs)"
rm -fr $dirpath
mkdir $dirpath

echo "Generate the test files (takes a few secs)"
# Work around argument list length restrictions
for year in {1800..1999}
do
    yearDir="${dirpath}/${year}"
    mkdir "$yearDir"
    for month in {01..12}
    do
        monthDir="${yearDir}/${month}"
        mkdir $monthDir
        touch "${monthDir}/main_${year}-${month}-"{01..28}".log"
    done
done
echo "Find 4 files among $(ls $dirpath | wc -l) directories"
echo " --- Python"
options="-n 100 -o 95 -t 2000-01-01 $dirpath"
hyperfine "./fdated.py $options >/dev/null"
echo " --- Go"
hyperfine "go-find-dated $options >/dev/null"
echo " --- GNU find"
hyperfine "find $dirpath -type f >/dev/null"
