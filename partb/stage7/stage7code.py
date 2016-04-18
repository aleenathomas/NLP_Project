import learn_classifier
import code_to_build_vocabulary
import bigrams
import re


# function to find the actual class of a given test sentence

def findclass(line):
	if line[-2:-1] == "+":
		return 1
	else:
		return 0
		
#find the count of a particular word in a class

def wordcount(filename,w1,w2,classname,bigram):
    wordnum = 0
    with open(filename) as datafile:
           for line in datafile: 
               if line[-2:-1] == classname:
               		words = line.split()
               		if(bigram == False):                       		
                       		for w in words:
		               		if w == w1:
				        	wordnum += 1
                	else:
                   		for i in range(len(words)-1):
                   			if w1==words[i] and w2 == words[i+1]:
                   				wordnum += 1	                              		               
    return wordnum
    
#find denominator for classcond.i.e sum of all features in class=clasname

def findden(filename,classname,vocfilename):
	bigram = 0
	unigram = 0
	
	vocfile = open(vocfilename,"r")
	
	for line in vocfile:
		
		count = len(re.findall(r'\w+', line))
		if(count==1):
			
    			if wordcount(filename,line,"",classname,False) > 0 :
				unigram+=1
		else:
			
			words = line.split()
			if wordcount(filename,words[0],words[1],classname,True) > 0 :
				bigram+=1
				
	return unigram + bigram
			
				
#find unigram count of a word w. If a word is present in some bigram , its unigram count is reduced accordingly

def unigramcount(filename,w,classname):
	ucount = 0
	bcount = 0
	datafile = open(filename,"r")
	for line in datafile:
		count = len(re.findall(r'\w+', line))
		if count==1 and w==line:
			ucount=+1
		elif count==2 and ( w == line[0] or w == line[1] ):
			bcount+=1
			
	return ucount-bcount 

   		
def class_cond(filename,w1,w2,classname, vocfilename,den):
    previousbigram=True			#previousbigram = True if the previous bigram was present in the vocabulary and False otherwise
    voc_num = learn_classifier.countwords(vocfilename)   
    num = wordcount(filename,w1,w2,classname,True)
    
    word = w1
    if num != 0:
    	previousbigram = True
        cond_prob = float(num + 1)/ ( den + voc_num )
    #else if the bigram is not present in the training set, then the corresponding unigram probabilities are found and multiplied  
    else:
    	previousbigram=False
        voc_num = learn_classifier.countunigrams(vocfilename)     #calculate the total numbre of unigrams in the vocabulary file  
        num = unigramcount(filename,w1,classname)	          #calculate the unigram count of the word w1 
        den = learn_classifier.wordcountclass(filename,classname) #total number of words in class=classname
        if(previousbigram==True):
        	cond_prob1 = float(num + 1)/ ( den + voc_num )
        else:
        	cond_prob1 = 1		 
        num = learn_classifier.wordcount(filename,w2,classname,False)       
        cond_prob2 = float(num + 1)/ ( den + voc_num )
        cond_prob = cond_prob1 * cond_prob2
   
    return cond_prob

def findclasscond(line,category,filename,den):
	words=line.split()
	prob=1
	for i in range(len(words)-1):
		prob*= class_cond(filename,words[i], words[i+1],category,"new_vocab.txt",den)
	return prob

def findposterior(line,category,filename,den):
	classconditionalprob = findclasscond(line,category, filename,den)
	posterior = classconditionalprob * learn_classifier.class_prior(filename,category)
	return posterior		
			
filename = "../../stage2/removed"
postotal = learn_classifier.classnum(filename, "+")
negtotal = learn_classifier.classnum(filename, "-")

datafile = open(filename,'r')
lines = datafile.readlines()

pbreak=0
nbreak=0
final_acc = 0
tr=["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10"]
te=["t1","t2","t3","t4","t5","t6","t7","t8","t9","t10"]
for k in range(10):
        #alg to test mixed data set
	
	testset = open(te[k],"w+")
	trainset = open(tr[k],"w+")
        if pbreak != 0:
		for index in range(0, pbreak+1):
			if findclass(lines[index]) == 1:
				trainset.write(lines[index])
	i = 0	
	if pbreak == 0:
		pj = pbreak
	else:
		pj = pbreak + 1
	
	while i < postotal/10:
		while (pj<postotal+negtotal):
			if findclass(lines[pj]) == 1:
				testset.write(lines[pj])
				pj = pj+1
				break
			pj = pj+1
		i = i+1
	pbreak = pj - 1
	
	for index in range(pbreak + 1, postotal+negtotal):
		if findclass(lines[index]) == 1:
			trainset.write(lines[index])
	#positives added
	if nbreak != 0:
		for index in range(0, nbreak+1):
			if findclass(lines[index]) == 0:
				trainset.write(lines[index])
	i = 0
	if nbreak == 0:
		nj = nbreak
	else:
		nj = nbreak + 1
	
	while i < negtotal/10:
		while (nj<postotal+negtotal):
			if findclass(lines[nj]) == 0:
				testset.write(lines[nj])
				nj = nj+1
				break
			nj = nj+1
		i = i+1
	nbreak = nj - 1
	
	for index in range(nbreak + 1, postotal+negtotal):
		if findclass(lines[index]) == 0:
			trainset.write(lines[index])
	#negatives added
	##end

	testset.close()	

	# code to train "train.txt"
	code_to_build_vocabulary.build_vocab(tr[k])	
	#call create_bigrams
	posden = findden(tr[k],'+',"new_vocab.txt")
	negden = findden(tr[k],'-',"new_vocab.txt")	

	bigrams.create_bigrams(tr[k]) 		
	learn_classifier.learn(tr[k], "new_vocab.txt") 

	# code to test the sentences in "test.txt"
	tp = 0 
	tn = 0
	fp = 0
	fn = 0

	with open(te[k]) as f: 
	    content = f.readlines()

	for line in content:
		
		post_pos = findposterior(line, "+", tr[k],posden) 	#find the posterior prob of positive 
		post_neg = findposterior(line, "-", tr[k],negden) 	#find the posterior prob of negative
		
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
