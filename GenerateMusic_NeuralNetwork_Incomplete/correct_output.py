# purpose: cleans the output (mostly from generated predictions) to remove duplicates (doesn't make sense to play the same note more than once in a chord), ignore any extra | or ! symbols, or sequences that don't begin with one of those. Finally, order chords by ascii, so something for example like "aeF6" is the same as "6Fea". Which should make similar sequences more similar

import re
import sys

file = sys.argv[1]

def remove_duplicates(word):
	# eg.  convert |FGGG!^7Fa to |7FG^a (ascii order, and removes extra | or !)
	start = word[0]
	word = word.replace('!','').replace('|','')
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

words = ''.join(words)

with open(f'{file}_cleaned', 'w') as f:
	f.write(words)
