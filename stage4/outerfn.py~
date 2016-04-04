#!/usr/bin/env python
import collections

vocabulary="../stage3code/vocabulary.txt"
removed="../stage2code /removed"
f=open(vocabulary,"r")
contents=f.read()
words = contents.split('\n')

#count the occurences of each distinct word in the file
keyword = collections.Counter()

#store the conditionalprob in dictionary 
#it stores a list of 2 elements: P(word|+) and P(word|-)

for word in words:
	pos_class_prob = class_cond(removed,word,'+')
	neg_class_prob = class_cond(removed,word,'-')
	keyword[word] = [pos_class_prob,neg_class_prob]
	
	
