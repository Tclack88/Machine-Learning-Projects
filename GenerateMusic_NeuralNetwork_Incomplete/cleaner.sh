#!/bin/bash
cat $1 | tr -d "[:blank:]" > tempfile && mv tempfile $1
cat $1 | tr [A-Z] [a-z] > tempfile && mv tempfile $1
awk '/note_on|note_off|tempo/' $1 > tempfile && mv tempfile $1
awk -F , 'NF=5' OFS=, $1 > tempfile && mv tempfile $1
