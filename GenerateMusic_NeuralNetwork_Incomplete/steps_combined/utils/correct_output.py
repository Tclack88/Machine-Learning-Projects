import re
import sys

file = sys.argv[1]

def remove_duplicates(word):
	# eg.  convert |FGGG!^7Fa to |7FG^a (ascii order, and removes extra | or !)
	start = word[0]
	word = word.replace('!','').replace('|','').replace("'",'')
	word = start + ''.join(list(set(word)))
	return word

with open(file, 'r') as f:
	content = f.read()

words = re.split(r'(\s+)',content)
for i, word in enumerate(words):
	if word.startswith('|') or word.startswith('!'):
		word = remove_duplicates(word)
	elif word.startswith(' '):
		pass
	else:
		word = ''
	words[i] = word

words = ''.join(words).lstrip() # remove leading space. fixes errors

with open(file, 'w') as f:
	f.write(words)
