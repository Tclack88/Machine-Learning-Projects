#!/usr/bin/env python3
# background #2e3436
import re
import sys

def sortstring(string):
    string = ''.join(sorted(string))
    return string

infile = sys.argv[1]
file = open(infile,'r')
text = file.read()
file.close
words = text.split(' ')

blank = ''
for j in words:
    if '|' in j:
        k= j.index('|')
        blank += ' '*int(j[0:k-1])
        blank += '|'+j[-1]
    elif '!' in j:
        k = j.index('!')
        blank += ' '*int(j[0:k-1])
        blank += '!'+j[-1]
    elif ' ' in j:
        j += ' '


tempwords = ''
words = re.split(r'(\S+)',blank)
words = list(filter(None,words))
# combine note_on's (|) and note off's (!)
k = 1
for word in words:
    if ' ' in word:
        tempwords += word
    else:
        while ("!" and "|" in word):
            j, k = 0, 1
            if word[j] == "|":
                tempword = word[j:k]
                while "!" not in tempword and k <= len(word):
                    k += 1
                    tempword = word[j:k]
                k -= 1
                tempword = word[j:k]
                tempwords += tempword+' '
                word = word[k:]
            elif word[j] == "!":
                tempword = word[j:k]
                while "|" not in tempword and k <= len(word):
                    k += 1
                    tempword = word[j:k]
                k -= 1
                tempword = word[j:k]
                tempwords += tempword+' '
                word = word[k:]
blank = ''
# findall instead of split because split returning empty entries
words = re.split(r'(\S+)',tempwords)
words = list(filter(None,words))
for word in words:
    if ' ' in word:
        blank += word
    else:
        char = word[0]
        word = word.replace(char,'')
        word = char+sortstring(word)
        blank += word+' ' #adds a space between these notes which were together, which is ok, it's a very short time period, also adds more time to the gap before.... oh well






# Save the results
outfile = str(sys.argv[1])+".enc"

file = open(outfile,"w")
file.write(blank)
file.close()
