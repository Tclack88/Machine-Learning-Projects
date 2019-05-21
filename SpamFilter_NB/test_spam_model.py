#!/usr/bin/env python3

# USAGE: call this file on file or directory to return predicted results

import pickle
from NBfunc import *
from spamkeys import sorted_spam_keys
import os
import sys

def TestModel(filepath,filename):
	test_matrix = CreateSingleFeatureMatrix(filepath,sorted_spam_keys) 
	result = int(loaded_model.predict(test_matrix))
	if result == 1:
		print(filename,"\t\t\t --     spam")
	elif result ==0:
		print(filename,"\t\t\t -- not spam")



spam_model = 'spam_model.sav'
loaded_model = pickle.load(open(spam_model,'rb'))



if os.path.isfile(sys.argv[1]):
	filename = sys.argv[1]
	filepath = filename
	TestModel(filepath, filename)
elif os.path.isdir(sys.argv[1]):
	dirname = sys.argv[1]
	for filename in os.listdir(dirname):
		filepath = dirname+"/"+filename
		TestModel(filepath, filename)
