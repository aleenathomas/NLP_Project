#!/usr/bin/env python
#training the classifier
from itertools import islice
import collections
import pickle
import math
import re

vocabulary="../stage6/vocabulary.txt"
removed="../stage6/removed"

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


   	
#find the count of a particular word in a class
def wordcount(filename,word,classname,bigram):
	wordnum = 0
	with open(filename) as datafile:
   		for line in datafile:
  
   			if line[-2:-1] == classname:
				if(bigram == False):
	   				words = line.split()
				else:
					#create bigrams from the line
					words = collections.Counter(zip(line, islice(line,1,None)))
					
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

#get the first word of the bigram
def getfirstword(bigram):
	return bigram.split(' ', 1)[0]	


				
#to find conditional probabilities
def class_cond(filename,bigram,classname):
	voc_num=countwords(vocabulary)
	
	num = wordcount(filename,bigram,classname,True)
	#wordcountclass function is not used here.
	word = getfirstword(bigram)
	den = wordcount(filename,word,classname,False)
	cond_prob = float(num + 1)/ ( den + voc_num )
	return cond_prob
		    	

def learn(filename,vocfilename):
	#make a list of all words and bigrams in the vocabulary
	f=open(vocfilename,"r")
	contents=f.read()
	words = contents.split('\n')
	f.close()


	#keyword is a dict indexed by each word in the vocabulary
	keyword = collections.Counter()

	#store the conditionalprob in dictionary 
	#it stores a list of 2 elements: log(P(word|+)) and log(P(word|-))
	
	for word in words:
		#checking whether the word is a bigram
		bigram = False
		count = len(re.findall(r'\w+', word))
		if(count==2):
			bigram = True
		if(bigram == True):
			pos_class_prob_log = math.log(class_cond(filename,word,'+'),2)
			neg_class_prob_log = math.log(class_cond(filename,word,'-'),2)
			keyword[word] = [pos_class_prob_log,neg_class_prob_log]

	#save the dict of learned probabilities in the file classifier.pickle

	with open('classifier.pickle', 'wb') as handle:
		pickle.dump(keyword, handle)
	f.close()
	
learn(removed,vocabulary)
#changed wordcount function,class_cond and learn function to make the algo work for bigrams
#used the formula P(sentence|class) = product of P(word-1,word | class) = count(word-1,word in class)+1 / count(word-1 in class) + size of vocabulary
#removed wordcountclass function
