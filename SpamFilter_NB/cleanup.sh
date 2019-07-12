#!/bin/bash
# used to remove unreadable bytes, the code is sensitive to non UTF-8 chars.
# It removes all characters except asci, tabs, carriage returns creating a 2nd file with ".clean" appended
# The contents of the "file.clean" is moved back to replace the original "file" then the "file.clean" is removed
usage()
{
        echo "Usage: $0 path/to/dir"
        exit 1
}

if [ $# -ne 1 ] ; then
        usage
else
for f in $1/*.txt; 
do $(tr -dc '\11\12\15\40-\176' < $f > $f.clean)
        mv $f.clean $f
        rm $f.clean -f
done
fi
