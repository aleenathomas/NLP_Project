import learn
import code_to_remove_stop_words
import code_to_build_vocabulary

# divide the set into 10
# using classnum, find the no. of reviews in pos and neg

def find_starting(classname):
	return 373

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
		prob*= learn.class_cond(filename,word,category)
	return prob

def findposterior(line,category,filename):
	classconditionalprob = findclasscond(line,category, filename)
	posterior = classconditionalprob * learn.class_prior(filename,category)
	return posterior		
			
filename = "../stage2code /removed"
postotal = learn.classnum(filename, "+")
negtotal = learn.classnum(filename, "-")

datafile = open(filename,'r')
lines = datafile.readlines()

for i in range(10):

	testset = open("test.txt","w+")
	trainset = open("train.txt","w+")

	pstart = 0
	pend = postotal/10

	for index in range(pstart, pend+1):
		testset.write(lines[index])
	for index in range(pstart+1):
		trainset.write(lines[index])		
	for index in range(pend+1, postotal):
		trainset.write(lines[index])		
	pstart = pstart + postotal/10
	pend = pend + postotal/10

	nstart = find_starting("-")
	nend = nstart + negtotal/10

	for index in range(nstart, nend+1):
		testset.write(lines[index])
	for index in range(find_starting("-"), nstart+1):
		trainset.write(lines[index])		
	for index in range(nend+1, find_starting("-") + negtotal):
		trainset.write(lines[index])		
	nstart = nstart + negtotal/10
	nend = nend + negtotal/10


	testset.close()	

	# code to train "train.txt"
	code_to_remove_stop_words.remove_stopwords("train.txt")
	code_to_build_vocabulary.build_vocab("removed")
	learn.learn("removed", "vocabulary.txt")

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
		print (str(actual)+" " +str(prediction))
					
	accuracy = float(tp + tn)/float(tp + tn + fp + fn)		
	print accuracy	


	trainset.close()
	f.close()	
