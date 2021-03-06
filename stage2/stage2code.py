#!/usr/bin/env python
#currently working with input as a text file and writing to another file!!!
import re
import collections
import os
#remove stop words
#convert all text to lowercase
#drop characters other than alphabets


#convert all to lowercase
review_file = open("../data.txt","r")
tempfile = open("temp.txt","r+")

lower_lines = [line.lower() for line in review_file]

tempfile.writelines(lower_lines)
tempfile.seek(0,0)

#removing stop words
sw_file = open("../stop_words","r")
stop_words = sw_file.readlines()
sw_file.close()


#remove '\n'	
stop_words = [word.strip('\n') for word in stop_words]

rem_file = open("removed", "w+")

#remove words
for l in tempfile:
	for word in stop_words:		
		l = re.sub(r'([^A-Za-z]|^)'+word+'([^A-Za-z]|$)', " ", l)
	
	rem_file.write(l)

review_file.close()

lines = []
#removing characters other than alphabets
rem_file.seek(0,0)
for l in rem_file:
	l = re.sub(r"[^A-Za-z\+\-\']", " ", l)	#to add space instead of specail characters except apostrophe
	l = re.sub(r"[\']", "", l)		#no space is added when apostrophe is removed
	l = re.sub(r'[\+]', "+"+"\n", l)		#add new line
	l = re.sub(r'[\-]', "-"+"\n", l)		#add new line
	lines.append(l)

#need to remove single letter words-not done yet!

rem_file.seek(0,0)
for line in lines:
	rem_file.write(line)

rem_file.close()
tempfile.close()
#os.remove("temp.txt")
