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
    	
voc_num=countwords('../stage3code/vocabulary.txt')


#datafile = open("../stage2code/removed", "r")

number_of_reviews = 0

with open("../stage2code /removed") as datafile:
    for line in datafile:
       if line.strip():
          number_of_reviews += 1

print 'number of number_of_reviews found %d' % number_of_reviews
