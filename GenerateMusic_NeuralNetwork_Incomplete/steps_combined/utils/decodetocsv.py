#!/usr/bin/env python3
import os
import pandas as pd
import sys

outfile = "step4.out"

# ascii-note-dictionary
asclist = []
keylist = []
for i in range(35,123):
    asclist.append(chr(i))
    keylist.append(i-14) #giving 21-108 as csvmidi encodes the midifiles

notedict = dict(zip(asclist,keylist))
#notedict[0] = ''
notedict['|'] = 'note_on_c'
notedict["!"] = 'note_off_c'
notedict["'"] = 'tempo'
notedict["{"] = 30

convertmeta = lambda x : notedict[x[0]]
convertnote = lambda x : notedict[x[1]]



# Decode back to csv
#infile = "convertmeback"
infile = sys.argv[1]

command = "cat "+infile+" | tr [' '] ['\\n'] > converted"

os.system(command)
os.system('echo "time~note\\n$(cat converted)" > converted')

df = pd.read_csv("converted",sep='~')
df['a'] = 1
df['b'] = df.time.apply(lambda x : x * 10).cumsum()
df['c'] = df.note.apply(convertmeta)
df['d'] = pd.NA
df.loc[df.c == "tempo", "d"] = df.note
df.loc[df.c == "tempo", "a"] = 1
df.d = df.d.str.extract(r'(\d+)').fillna(0)
df['e'] = df.note.apply(convertnote)
df['f'] = 50
df.drop(["time","note"],axis=1,inplace=True)
df.to_csv(outfile,index=False,header=False)
os.system(f'echo "0,0,header,0,1,480\n1,0,start_track\n$(cat {outfile})" > {outfile}')

import subprocess


#end_time = int(subprocess.check_output('tail -1 final | grep -Eo "[0-9]{3,}"',shell=True))
#command = "echo '1,"+str(end_time)+",end_track\n0,0,end_of_file' >> final"
command = f"tail -1 {outfile} "+" | awk -F, '{print $2}'"
end_time = int(subprocess.check_output(command, shell=True))
command = "echo '1,"+str(end_time)+f",end_track\n0,0,end_of_file' >> {outfile}"
os.system(command)

