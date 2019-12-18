#!/usr/bin/env python3

import re
import sys

infile = sys.argv[1]

file = open(infile,"r")
text = file.read()
file.close()

text = text.strip()

words = re.split(r'(\s+)',text)

# split notes up to fit the original ecryption scheme
for word in words:
    if ' ' not in word:
        word = list(word)
        word = list(''.join(word))
    print(word)


blank = ''

for k in range(len(words[0])):
    blank += '0~|'+words[0][k]+" "
pairs = zip(words[1::2],words[2::2])
#print(pairs)
for j in pairs:
    for k in range(len(j[1])):
        if k == 0:
            blank += str(len(j[0]))+"~|"+str(j[1][k])+" "
        else:
            blank +="0~|"+str(j[1][k]+" ")
#print(blank)

#save file
file = open("decoded.txt",'w')
file.write(blank)
file.close()
