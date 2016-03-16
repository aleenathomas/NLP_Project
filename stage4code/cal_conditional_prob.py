#!/usr/bin/env python
import re

#P(x|+)=(count(x,+) + 1)/(countofwords(+) + noofwords(vocabulory))

def conditionalprobforpos(word,category):
	textfile = open ("../stage2code /removed", 'r')
	matches = []
	reg = re.compile(word + ".*\\" + category + "$")
	for line in textfile:
	    matches += reg.findall(line)
	print(len(matches))
	textfile.close()
			
conditionalprobforpos("good","+")
conditionalprobforpos("good","-")
