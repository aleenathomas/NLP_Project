from itertools import islice
import collections
def create_bigrams(filename):
	infile = open("bigram_file","r")
	contents = infile.read()
	words = contents.split()
	bigrams = collections.Counter(zip(words, islice(words,1,None)))

	infile.close()
	infile = open("dist_bigrams","w")
	for word in bigrams:
		if bigrams[word] >= 3:
			infile.write(" ".join(word))
			infile.write("\n")

