import learn

# divide the set into 10
# using classnum, find the no. of reviews in pos and neg
# 

def find_starting(classname):
	return 352

# function to find the actual class of a given test sentence
def findclass(line):
	if line[-2:-1] == "+":
		return 1
	else
		return 0
			
filename = "../stage2code /removed"
postotal = learn.classnum(filename, "+")
negtotal = learn.classnum(filename, "-")

datafile = open(filename,'r')
lines = datafile.readlines()

testset = open("test.txt","r+")
trainset = open("train.txt","r+")

start = 0
end = postotal/10

for index in range(start, end+1):
	testset.write(lines[index])
for index in range(start+1):
	trainset.write(lines[index])		
for index in range(end+1, postotal):
	trainset.write(lines[index])		
start = start + postotal/10
end = end + postotal/10

start = find_starting("-")
end = negtotal/10

for index in range(start, end+1):
	testset.write(lines[index])
for index in range(start+1):
	trainset.write(lines[index])		
for index in range(end+1, postotal):
	trainset.write(lines[index])		
start = start + negtotal/10
end = end + negtotal/10
	
# code to train "train.txt"


# code to test the sentences in "test.txt"
tp = 0 
tn = 0
fp = 0
fn = 0
contents = testset.read()
lines = contents.split('\n')
for line in lines:	
	post_pos = findposterior(line, "+")	#find the posterior prob of positive 
	post_neg = findposterior(line, "-")	#find the posterior prob of negative
	if post_pos > post_neg:			#predict
		prediction = 1
	else 
		prediction = 0
	actual = findclass(line)	
	if  actual == 1 and prediction == 1:
		tp += 1	
	else if  actual == 0 and prediction == 0:
		tn += 1
	else if  actual == 0 and prediction == 1:
		fp += 1	
	else 
		fn +=1		
accuracy = float(tp + tn)/float(tp + tn + fp + fn)		
print accuracy	
testset.close()
trainset.close()	
