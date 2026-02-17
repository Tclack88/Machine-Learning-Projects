#!/usr/bin/env python3

import os
import sys
import pandas as pd

#Create Ascii-Note dictionary
asclist = []
keylist = []
for i in range(35,123):
    asclist.append(chr(i))
    keylist.append(i-14) #giving 21-108 as csvmidi encodes the midifiles

notedict = dict(zip(keylist,asclist))
notedict[0] = ''
notedict['note_on_c']='|'
notedict['note_off_c']='!'
notedict['tempo']="'"
notedict[30] = '{' # because this was a comma, but pandas places quotes around everything in that line

symbToAscii = lambda x: notedict[x]
print(notedict)



# open song, clean, convert to word text
#command = "cleaner.sh "+str(sys.argv[1])
infile = str(sys.argv[1])
command = "./cleaner.sh "+infile
os.system(command)

command = 'echo  "a,b,c,d,e,f\\n$(cat '+infile+')" > '+infile 
                 # normally need a '-e' after echo,
                 # but python is taking care of it
                 # somehow... oh well


outfile = infile+".out"

os.system(command)
df = pd.read_csv(infile)
df = df.drop(['a','f'],axis=1)
df.b = df.b.diff().fillna(0).astype(int)
df = df.round({'b':-1})
df.e = df.e.fillna(0).astype(int) #tempo has blank for col e. Filling with 0's works
df['out'] = df['b'].apply(lambda x: x //10).astype(str)+'~'+df['c'].apply(symbToAscii)+df['e'].apply(symbToAscii)
df.loc[df.c == 'tempo','out'] += str(df.loc[df.c == 'tempo','d'].iloc[0].astype(int))
df["out"].to_csv(outfile,index=False)
print(df.head(20))

command = "cat "+outfile+" | tr ['\\n'] [' '] > tempfile && mv tempfile "+outfile
os.system(command)

