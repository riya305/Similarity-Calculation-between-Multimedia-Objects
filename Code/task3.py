import csv
import datetime
import math
import pandas as pd
from scipy.spatial.distance import cosine
import numpy as np
from scipy.spatial import distance
from heapq import nsmallest
from lxml import etree
import sys


def euclidean_distance(X, Y):
	return math.sqrt(sum((X.get(d,0) - Y.get(d,0))**2 for d in set(X) | set(Y)))

def union2(dict1, dict2):
    return dict(list(dict1.items()) + list(dict2.items()))

def cosine_similarity(v1,v2):
    #"compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"

    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    # extracting 3 max terms contributing most to the similarity can't be picked in case of cosine similarity
    # as it normalizes the vector
    return sumxy/math.sqrt(sumxx*sumyy)

def cosine_dic(dic1,dic2):
    numerator = 0
    dena = 0
    for key1,val1 in dic1:
        numerator += val1*dic2.get(key1,0.0)
        dena += va1*val1
    denb = 0
    for val2 in dic2.values():
        denb += val2*val2
    return numerator/math.sqrt(dena*denb)

def main():
	#Load text file into list with CSV module
	# with open('/home/riya/Downloads/MWDB/desctxt/onewordPOI.txt', 'rt') as f:
	# 	reader = csv.reader(f, delimiter = ' ', skipinitialspace=True)
	# 	lineData = list()
	# 	cols = next(reader)

	# 	for line in reader:
	# 		if line != []:
	# 			lineData.append(line)


	# with open('/home/riya/Downloads/MWDB/desctxt/twowordsPOI.txt', 'rt') as f:
	# 	reader = csv.reader(f, delimiter = ' ', skipinitialspace=True)
	# 	lineData2 = list()
	# 	cols = next(reader)

	# 	for line in reader:
	# 		if line != []:
	# 			lineData2.append(line)

	# with open('/home/riya/Downloads/MWDB/desctxt/threewordsPOI.txt', 'rt') as f:
	# 	reader = csv.reader(f, delimiter = ' ', skipinitialspace=True)
	# 	lineData3 = list()
	# 	cols = next(reader)

	# 	for line in reader:
	# 		if line != []:
	# 			lineData3.append(line)

	# with open('/home/riya/Downloads/MWDB/desctxt/fourwordsPOI.txt', 'rt') as f:
	# 	reader = csv.reader(f, delimiter = ' ', skipinitialspace=True)
	# 	lineData4 = list()
	# 	cols = next(reader)

	# 	for line in reader:
	# 		if line != []:
	# 			lineData4.append(line)

	giventermdict = {}
	elemdict = {}
	listPerUser1 = []
	listPerUser2 = []
	givendict = {}
	userlist1=[]
	userlist2=[]
	temptermdict={}

	loc_id = sys.argv[1]
	model = sys.argv[2]
	k = sys.argv[3]
	flag=0

	doc = etree.parse("/home/riya/Code/devset_topics.xml")

	topicElem = doc.getroot()
	locIdNameDict={}
	for topic in topicElem:
		locIdNameDict[topic[0].text]= topic[1].text.replace("_"," ")
	with open('/home/riya/Code/desctxt2/devset_textTermsPerPOI.wFolderNames.txt', 'rt') as f:
		reader = csv.reader(f, delimiter = ' ', skipinitialspace=False)
		lineData = list()
		cols = next(reader)
		
		for line in reader:
			loc_name=" ".join(line[0].split("_"))
			startIndex=len(line[0].split("_"))
			newIndex=startIndex*2

			if(locIdNameDict[loc_id]==loc_name):
				given_loc=line[newIndex-startIndex+1:]
				givendict[loc_id]=given_loc
			else:
				elemdict[loc_name]=line[newIndex-startIndex+1:]


		
	#Change every item in the sub list into the correct data type and store it in a directory
	# print(givendict)
	givenArr=givendict[loc_id]
	i=0
	giventermdict={}
	while(i < len(givenArr)-1):
		if(model=="TF"):
			giventermdict[givenArr[i]]=int(givenArr[i+1])
		elif(model=="DF"):
			giventermdict[givenArr[i]]=int(givenArr[i+2])
		else:
			giventermdict[givenArr[i]]=float(givenArr[i+3])
		i=i+4
	givendict[loc_id]=giventermdict


	for key, value in elemdict.items():
		locArr=value
		i=0
		elemtermdict={}
		while(i < len(locArr)-1):
			if(model=="TF"):
				elemtermdict[locArr[i]]=int(locArr[i+1])
			elif(model=="DF"):
				elemtermdict[locArr[i]]=int(locArr[i+2])
			else:
				elemtermdict[locArr[i]]=float(locArr[i+3])
			i=i+4
		elemdict[key]=elemtermdict
				
	
	for key, value in elemdict.items():
		termScoredict={}
		temptermdict=giventermdict
		for term,TF in value.items():

			if(term not in giventermdict):
				temptermdict[term]=0
			else:
				if(model=="TF"):
					termScoredict[term]=giventermdict[term]*(abs(giventermdict[term]-TF))
				else:
					termScoredict[term]=(abs(giventermdict[term]-TF))/(giventermdict[term]+1)

		for term,TF in giventermdict.items():
			if(term not in value):
				value[term]=0
		
		similarityScore2=euclidean_distance(value,temptermdict)
		
		three_smallest = nsmallest(3, termScoredict, key=termScoredict.get)
	
		listPerUser2.append({"ID": key, "Score" :similarityScore2, "Terms": three_smallest})

	# # userlist1 = sorted(listPerUser1, key=lambda k: k['Score'], reverse=True)
	userlist2 = sorted(listPerUser2, key=lambda k: k['Score'], reverse=False)

	# # print("********************Cos distance*****************\n")
	# # i=0
	# # while i < int(k):
	# # 	print(userlist1[i])
	# # 	i=i+1

	print("********************L2 distance*****************\n")
	i=0
	while i < int(k):
		print(userlist2[i])
		i=i+1

main()

