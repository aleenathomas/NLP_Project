#!/usr/bin/env python
#training the classifier

import collections
import pickle
import math

vocabulary="../stage3code/vocabulary.txt"
removed="../stage2code /removed"

#function to count the number of words in a file(vocabulary)
def countwords(filename):
	f = open(filename, "r+")
	contents=f.read()
	words=contents.split()
	
	count = 0
	for word in words:
        	count += 1
        f.close()
    	return count
    	
    	
#function to count the number of reviews
def countnumofreviews(filename):
	number_of_reviews = 0
	with open(filename) as datafile:
   		for line in datafile:
        		if line.strip():
        			number_of_reviews += 1
        	
        return number_of_reviews
#to find the number of reviews in each class
def classnum(filename,classname):
	num = 0
	with open(filename) as datafile:
   		for line in datafile:
  
   			if line[-2:-1] == classname:
   				num = num + 1
   				
   	return num

#to find the number of words in each class   	
def wordcountclass(filename,classname):
	wordnum = 0
	with open(filename) as datafile:
   		for line in datafile:
  
   			if line[-2:-1] == classname:
   				wordnum += len(line.split()) - 1
   				
   	return wordnum   
   	
#find the count of a particular word in a class
def wordcount(filename,word,classname):
	wordnum = 0
	with open(filename) as datafile:
   		for line in datafile:
  
   			if line[-2:-1] == classname:
   				words = line.split()
   				for w in words:
   					if w == word:
   						wordnum += 1 
   				
   	return wordnum  
   	
#to find prior probabilities
def class_prior(filename,classname):
	number_of_reviews = countnumofreviews(filename)
	num = classnum(filename,classname)	
	prior = (float)(num)/number_of_reviews
	return prior
				
#to find conditional probabilities
def class_cond(filename,word,classname):
	voc_num=countwords(vocabulary)
	num = wordcount(filename,word,classname)
	den = wordcountclass(filename,classname)
	cond_prob = float(num + 1)/ ( den + voc_num )
	return cond_prob
		    	

def learn(filename,vocfilename):
	#make a list of all words in vocabulary
	f=open(vocfilename,"r")
	contents=f.read()
	words = contents.split('\n')
	f.close()


	#keyword is a dict indexed by each word in the vocabulary
	keyword = collections.Counter()

	#store the conditionalprob in dictionary 
	#it stores a list of 2 elements: log(P(word|+)) and log(P(word|-))

	for word in words:
		pos_class_prob_log = math.log(class_cond(filename,word,'+'),2)
		neg_class_prob_log = math.log(class_cond(filename,word,'-'),2)
		keyword[word] = [pos_class_prob_log,neg_class_prob_log]

	#save the dict of learned probabilities in the file classifier.pickle

	with open('classifier.pickle', 'wb') as handle:
		pickle.dump(keyword, handle)
	f.close()
	
learn(removed,vocabulary)
