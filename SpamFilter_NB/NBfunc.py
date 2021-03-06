#!/usr/bin/env python3

# First working version completed 19May 2019 in 2 days
# (original attempt squandered from stolen laptop :/ ) 

import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix



# Takes a line (string), remove \n and non-alphanumeric chars,
# creates list split on spaces, removes empty list entries
# lessons learned: filter removes 'False' entries
# so 'None' is True and thus stays
def Filter(line):
	filtered = list(filter(None,re.sub('[^a-zA-Z $]','',line.strip('\n')).split(' ')))
	return filtered
# TODO: consider in bash changing original emails "don ' t " with "don't" etc. 
# and keeping the ' symbols


# returns a filtered list of words in email
def SplitEmail(File):
	inner_list = []
	with open(File) as email:
		for line in email:
			line = Filter(line)
			inner_list += line
	return inner_list

#makes a frequency dictionary with a list, removes stopwords
# TODO: consider removing common words:
# "http, com Subject, html, original message, email, s, t,.." etc...
def MakeEmailDict(word_list):
	email_dict = Counter()
	for word in word_list:
		if word in stop_words:
			pass
		else:
			email_dict[word] += 1
	return email_dict

# Make a frequency list, returns the most common words found.
# Returns list of tuples NOTE:(dict() to gets back as dictionary)
def MakeSpamDict(train_data):
	with open(train_data) as f:
		all_word_list = []
		for File in f:
			all_word_list += SplitEmail(File.strip('\n'))
		spam_dictionary = MakeEmailDict(all_word_list)	
		return dict(spam_dictionary.most_common(5000))


#Creates array of 0 and 1, where 1 is spam, 0 is not
def CreateSpamLabels(train_data):
	spam_labels = []
	with open(train_data) as f:
		for line in f:
			line = line.strip('\n')
			if line[-7:] == 'pam.txt':
				spam_labels.append(1)
			else:
				spam_labels.append(0)
	return np.asarray(spam_labels)

# used for single file instead of file containing list of files
def CreateSingleFeatureMatrix(train_data,sorted_spam_keys):
	spam_matrix = []
	word_list = SplitEmail(train_data)
	word_dict = MakeEmailDict(word_list)
	sorted_word_dict = sorted(k for (k,v) in word_dict.items())
	spam_vector = np.zeros(len(sorted_spam_keys))
	for i in range(len(spam_vector)):
		if sorted_spam_keys[i] in sorted_word_dict:
			spam_vector[i] = word_dict[sorted_spam_keys[i]]
	spam_matrix.append(spam_vector)
	return np.asarray(spam_matrix)

#  used for file containing list of file names
def CreateFeatureMatrix(train_data,sorted_spam_keys):
	spam_matrix = []
	with open(train_data) as f:
		for File in f:
			word_list = SplitEmail(File.strip('\n'))
			word_dict = MakeEmailDict(word_list)
			sorted_word_dict = sorted(k for (k,v) in word_dict.items())
			spam_vector = np.zeros(len(sorted_spam_keys))
			for i in range(len(spam_vector)):
				if sorted_spam_keys[i] in sorted_word_dict:
					spam_vector[i] = word_dict[sorted_spam_keys[i]]
			spam_matrix.append(spam_vector)
	return np.asarray(spam_matrix)


stop_words = set(stopwords.words('english'))

