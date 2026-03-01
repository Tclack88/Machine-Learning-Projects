#!/usr/bin/env python3

import re
import sys
#infile = "encoded.txt"
infile = sys.argv[1]

file = open(infile,"r")
text = file.read()
file.close()

words = re.split(r'(\s+)',text)
words = [w for w in words if w] # remove empty lines

# split notes up to fit the original ecryption scheme
blank = "0~'500000 " # standard tempo

pairs = zip(words[0::2],words[1::2])

for pair in list(pairs):
	duration = len(pair[0])
	symbol = pair[1][0] # ! or |
	notes = pair[1][1:] # cluster of "notes" eg.. MRV, (or singular if len 1)
	if len(notes) == 1:
		blank += str(duration)+'~'+symbol+notes+' '
	else:
		for n,note in enumerate(notes):
			if n == 0:
				blank += str(duration)+'~'+symbol+note
			else:
				blank += "0~"+symbol+note
			blank += ' ' # trailing space

#print(blank)

#save file
file = open("step3.out",'w')
file.write(blank)
file.close()
