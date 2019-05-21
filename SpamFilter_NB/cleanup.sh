#!/bin/bash
# used to remove unreadable bytes, the code is sensitive to non UTF-8 chars.
# 1st line removes all characters except asci, tabs, carriage returns 
# 2nd line removes the old files (i.e. without the prepended "cleaned.")
# 3rd line renames the old files back to their original names
for f in *.txt; do $(tr -cd '\11\12\15\40-\176' < $f > cleaned.$f); done
find . -type f ! -name "clean*" -exec rm {} \;
for f in cleaned*.txt; do mv $f ${f##cleaned.}; done
