import learn_classifier
import code_to_remove_stop_words
import code_to_build_vocabulary

# divide the set into 10
# using classnum, find the no. of reviews in pos and neg

# function to find the actual class of a given test sentence
def findclass(line):
	if line[-2:-1] == "+":
		return 1
	else:
		return 0

def findclasscond(line,category,filename):
	words=line.split()
	prob=1
	for word in words:
		prob*= learn_classifier.class_cond(filename,word,category)
	return prob

def findposterior(line,category,filename):
	classconditionalprob = findclasscond(line,category, filename)
	posterior = classconditionalprob * learn_classifier.class_prior(filename,category)
	return posterior		
			
filename = "../stage6/removed"
postotal = learn_classifier.classnum(filename, "+")
negtotal = learn_classifier.classnum(filename, "-")

datafile = open(filename,'r')
lines = datafile.readlines()

pbreak=0
nbreak=0
final_acc = 0
for k in range(10):
        #alg to test mixed data set

	testset = open("test.txt","w+")
	trainset = open("train.txt","w+")
        if pbreak != 0:
		for index in range(0, pbreak+1):
			if findclass(lines[index]) == 1:
				trainset.write(lines[index])
	i = 0	
	pj = pbreak
	while i < postotal/10:
		while (pj<postotal+negtotal):
			if findclass(lines[pj]) == 1:
				testset.write(lines[pj])
				pj = pj+1
				break
			pj = pj+1
		i = i+1
	pbreak = pj
	for index in range(pbreak + 1, postotal+negtotal):
		if findclass(lines[index]) == 1:
			trainset.write(lines[index])
	#positives added
	if nbreak != 0:
		for index in range(0, nbreak+1):
			if findclass(lines[index]) == 0:
				trainset.write(lines[index])
	i = 0
	nj = nbreak
	while i < negtotal/10:
		while (nj<postotal+negtotal):
			if findclass(lines[nj]) == 0:
				testset.write(lines[nj])
				nj = nj+1
				break
			nj = nj+1
		i = i+1
	nbreak = nj
	for index in range(nbreak + 1, postotal+negtotal):
		if findclass(lines[index]) == 0:
			trainset.write(lines[index])
	#negatives added
	##end

	testset.close()	

	# code to train "train.txt"
	code_to_remove_stop_words.remove_stopwords("train.txt")
	code_to_build_vocabulary.build_vocab("removed")
	#call create_bigrams
	learn_classifier.learn("removed", "new_vocab.txt")

	# code to test the sentences in "test.txt"
	tp = 0 
	tn = 0
	fp = 0
	fn = 0

	#contents = testset.read()
	#lines = contents.split('\n')

	#print len(lines)

	with open("test.txt") as f:
	    content = f.readlines()

	for line in content:	
		post_pos = findposterior(line, "+", "removed")	#find the posterior prob of positive 
		post_neg = findposterior(line, "-", "removed")	#find the posterior prob of negative
		if post_pos > post_neg:			#predict
			prediction = 1
		else: 
			prediction = 0
		actual = findclass(line)	
		if  actual == 1 and prediction == 1:
			tp += 1	
		elif  actual == 0 and prediction == 0:
			tn += 1
		elif  actual == 0 and prediction == 1:
			fp += 1	
		else: 
			fn +=1	
		#print (str(actual)+" " +str(prediction))
					
	accuracy = float(tp + tn)/float(tp + tn + fp + fn)		
	print accuracy	
	final_acc = final_acc + accuracy

	trainset.close()
	f.close()	
print "final accuracy = " + str(final_acc/10)
