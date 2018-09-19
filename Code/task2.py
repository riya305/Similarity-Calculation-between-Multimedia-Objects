import csv
import datetime
import math
import pandas as pd
from scipy.spatial.distance import cosine
import numpy as np
from scipy.spatial import distance
from heapq import nsmallest
import sys

def euclidean_distance(X, Y):
	
	# return distance.euclidean(a, b)
	return math.sqrt(sum((X.get(d,0) - Y.get(d,0))**2 for d in set(X) | set(Y)))
	# return (np.linalg.norm(x-y))

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
	with open('/home/riya/Code/desctxt2/devset_textTermsPerImage.txt', 'rt') as f:
		reader = csv.reader(f, delimiter = ' ', skipinitialspace=False)
		lineData = list()
		cols = next(reader)

		for line in reader:
			if line != []:
				lineData.append(line)

	giventermdict = {}
	elemdict = {}
	listPerUser1 = []
	listPerUser2 = []
	givendict = {}
	userlist1=[]
	userlist2=[]
	temptermdict={}

	user_id = sys.argv[1]
	model = sys.argv[2]
	k = sys.argv[3]
	flag=0
	userID=""
	#Poplulating the dictionary
	for i in range(len(lineData)):
		noOfTerms = (len(lineData[i])-2)/4
		temp = 1
		elemtermdict={}
		for j in range(int(noOfTerms)):
			term = lineData[i][temp].replace('"','')
			if(lineData[i][0]==user_id):
				if(model=="TF"):
					giventermdict[term]=int(lineData[i][temp+1])
				elif(model=="DF"):
					giventermdict[term]=int(lineData[i][temp+2])
				else:
					giventermdict[term]= float(lineData[i][temp+3])
				flag=1
			else:
				flag=0
				if(model=="TF"):
					elemtermdict[term]=int(lineData[i][temp+1])
				elif(model=="DF"):
					elemtermdict[term]=int(lineData[i][temp+2])
				else:
					elemtermdict[term]= float(lineData[i][temp+3])

			temp=temp+4

		if(flag==1):
			givendict[user_id]=giventermdict
		else:
			elemdict[lineData[i][0]]=elemtermdict
	
	############### most similar terms calculation ##################
	for key, value in elemdict.items():
		termScoredict={}
		temptermdict=giventermdict
		for term,TF in value.items():
			if(term not in giventermdict):
				temptermdict[term]=0
			else:
				termScoredict[term]=giventermdict[term]*(abs(giventermdict[term]-TF))

		for term,TF in giventermdict.items():
			if(term not in value):
				value[term]=0

		################ three_smallest###############
		similarityScore2=euclidean_distance(value,temptermdict)
		three_smallest = nsmallest(3, termScoredict, key=termScoredict.get)
		listPerUser2.append({"ID": key, "Score" :similarityScore2, "Terms": three_smallest})

	############# Sorted #########################
	userlist2 = sorted(listPerUser2, key=lambda k: k['Score'], reverse=False)


	print("********************L2 distance*****************\n")
	i=0
	while i < int(k):
		print(userlist2[i])
		i=i+1

main()

