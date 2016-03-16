#!/usr/bin/env python
#training the classifier

import collections


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
    	
    	
def countnumofreviews(filename):
	number_of_reviews = 0
	with open(filename) as datafile:
   		for line in datafile:
        		if line.strip():
        			number_of_reviews += 1
        	
        return number_of_reviews
    	
voc_num=countwords('../stage3code/vocabulary.txt')
number_of_reviews = countnumofreviews("../stage2code /removed")
print 'number of number_of_reviews found %d' % number_of_reviews
