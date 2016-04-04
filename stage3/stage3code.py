#!/usr/bin/env python
#code to build the vocabulary
import re
import collections

rem_file = open("../stage2/removed", "r")

#additional-make a list of words from the file
rem_file.seek(0,0)
contents = rem_file.read()
words = contents.split()

#count the occurences of each distinct word in the file
count = collections.Counter()
for word in words:
	count[word] = count[word] + 1

#write into vocabulary file those words that have count>=2
vocab = open("vocabulary.txt","w")
for word in count:
	if count[word] >= 2:
		vocab.write(word+"\n")	

vocab.close()
rem_file.close()
