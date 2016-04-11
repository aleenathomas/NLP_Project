from itertools import islice
import code_to_build_vocabulary
import collections
import re

def create_bigrams(filename):
	infile = open(filename,"r")
	contents = infile.read()
	words = contents.split()
	#create bigrams from the file
	bigrams = collections.Counter(zip(words, islice(words,1,None)))

	infile.close()
	#add bigrams with count>=3 to vocabulary
	infile = open("vocabulary.txt","a+")
	for word in bigrams:
		if bigrams[word] >= 2:
			infile.write(" ".join(word))
			infile.write("\n")
	#remove bigrams starting and ending with + or - from vocabulary
	vocab = open("new_vocab.txt","w")
	infile.seek(0,0)
	for line in infile:
		if(not line.startswith('+') and not line.startswith('-') and not line[-2:-1] == '+' and not line[-2:-1] == '-'):
			vocab.write(line)
		
	infile.close()
	vocab.close()

create_bigrams("../../stage2/removed")
