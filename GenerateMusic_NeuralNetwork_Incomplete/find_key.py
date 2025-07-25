import matplotlib.pyplot as plt

files = """
chopin_op28_1.mid.csv.out.enc
chopin_op28_10.mid.csv.out.enc
chopin_op28_11.mid.csv.out.enc
chopin_op28_12.mid.csv.out.enc
chopin_op28_13.mid.csv.out.enc
chopin_op28_14.mid.csv.out.enc
chopin_op28_15.mid.csv.out.enc
chopin_op28_16.mid.csv.out.enc
chopin_op28_17.mid.csv.out.enc
chopin_op28_18.mid.csv.out.enc
chopin_op28_19.mid.csv.out.enc
chopin_op28_2.mid.csv.out.enc
chopin_op28_20.mid.csv.out.enc
chopin_op28_21.mid.csv.out.enc
chopin_op28_22.mid.csv.out.enc
chopin_op28_23.mid.csv.out.enc
chopin_op28_24.mid.csv.out.enc
chopin_op28_3.mid.csv.out.enc
chopin_op28_4.mid.csv.out.enc
chopin_op28_5.mid.csv.out.enc
chopin_op28_6.mid.csv.out.enc
chopin_op28_7.mid.csv.out.enc
chopin_op28_8.mid.csv.out.enc
chopin_op28_9.mid.csv.out.enc
""".split()

song_keys = """
'Prélude op. 28 no. 2 in A minor.mp3'*		C (Am)
'Prélude op. 28 no. 4 in E minor.mp3'*		G (Em)
'Prélude op. 28 no. 6 in B minor.mp3'*		D (Bm)
'Prélude op. 28 no. 7 in A major.mp3'*		A (F#m)
'Prélude op. 28 no. 8 in F# minor.mp3'*		A (F#m)
'Prélude op. 28 no. 9 in E major.mp3'*		E (C#m)
'Prélude op. 28 no. 12 in G# minor.mp3'*	B (G#m)
'Prélude op. 28 no. 13 in F# major.mp3'*	F# (Ebm)
'Prélude op. 28 no. 14 in Eb minor.mp3'*	F# (Ebm)
'Prélude op. 28 no. 15 in Db minor.mp3'*	E  (Dbm)
'Prélude op. 28 no. 16 in Bb minor.mp3'*	C# (A#m)
'Prélude op. 28 no. 17 in Ab major.mp3'*	G# (Fm)
'Prélude op. 28 no. 18 in F minor.mp3'*		G# (Fm)
'Prélude op. 28 no. 19 in Eb major.mp3'*	D# (Cm)
'Prélude op. 28 no. 20 in C minor.mp3'*		D# (Cm)
'Prélude op. 28 no. 22 in G minor.mp3'*		A# (Gm)
'Prélude op. 28 no. 24 in D minor.mp3'*		F (Dm)
'Prélude op. 45 in C# minor .mp3'*			E (C#m)
"""


file_in = "chopin_op28_24.mid.csv.out.enc"

asclist = [chr(i) for i in range(35,123)] # the range of ascii chars mapped to piano notes
asclist[9] = "{"
#import sys; sys.exit(0)
keylist = "A A# B C C# D D# E F F# G G#".split()*7 + "A A# B C".split()

asc_keymap = dict(zip(asclist,keylist))



def add(notes):
	for note in notes:
		"""
		if count_dict.get(note, None) == None:
			count_dict[note] = 1
		else:
			count_dict[note] += 1
		"""
		key = asc_keymap[note]
		if count_dict.get(key, None) == None:
			count_dict[key] = 1
		else:
			count_dict[key] += 1
		

print(song_keys)
files = ['chopin_op28_2.mid.csv.out.enc']

for file_in in files:
	count_dict = {}
	with open(file_in) as f:
		for line in f:
			for notes in line.split():
				if notes[0] == "|":
					add(notes[1:])

	count_dict = dict(sorted(count_dict.items(), key=lambda x: x[0]))
	X = count_dict.keys()
	Y = count_dict.values()
	Y = [y/sum(Y) for y in Y]
	plt.bar(X,Y)
	plt.title(file_in)
	plt.show()
#asc_keymap = {'D': 195, 'A': 255, 'F': 187, 'C': 137, 'A#': 61, 'E': 150, 'B': 81, 'G': 123, 'D#': 28, 'G#': 72, 'F#': 39, 'C#': 45}
		
#asc_keymap = dict(sorted(asc_keymap.items(), key=lambda x: x[0]))
