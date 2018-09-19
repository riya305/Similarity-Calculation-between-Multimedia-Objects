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


def euclidean_distance(v1, v2):
	x = np.array(v1)
	y = np.array(v2)
	# return distance.euclidean(a, b)
	return (np.linalg.norm(x-y))

def L1_distance(v1, v2):
	L1 = 0
	for i in range(len(v1)):
		L1=L1+abs(v1[i]-v2[i])
	# return distance.euclidean(a, b)
	return (L1)

def union2(dict1, dict2):
    return dict(list(dict1.items()) + list(dict2.items()))

def cosine_similarity(v1,v2):
    #"compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"

    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = float(v1[i]); 
        y = float(v2[i])
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
	listPerUser1 = []
	listPerUser2 = []
	givenObj=""
	userlist1=[]
	userlist2=[]
	locdict2={}

	loc_id = sys.argv[1]
	model = sys.argv[2]
	k = sys.argv[3]
	flag=0
	userID=""
	doc = etree.parse("/home/riya/Code/devset_topics.xml")
	######################## Reading from the csv files############################s
	topicElem = doc.getroot()
	for topic in topicElem:
		if(loc_id==topic[0].text):

			with open('/home/riya/Code/descvis/img/'+topic[1].text+' '+model+'.csv', 'rt') as f:
				reader = csv.reader(f, delimiter = ',', skipinitialspace=True)
				lineData = list()
				cols = next(reader)
				for line in reader:
					if line != []:
						# imagedict[line[0]]=line[1:]
						lineData.append({"imgID":line[0],"imgVectors":line[1:]})
			loc_name = topic[1].text.replace("_"," ")
			givenObj={"loc_name":loc_name,"imageList":lineData}
		else:
			with open('/home/riya/Code/descvis/img/'+topic[1].text+' '+model+'.csv', 'rt') as f:
				reader = csv.reader(f, delimiter = ',', skipinitialspace=True)
				lineData2 = list()
				cols = next(reader)
				for line in reader:
					if line != []:
						# imagedict[line[0]]=line[1:]
						lineData2.append({"imgID":line[0],"imgVectors":line[1:]})
			loc_name = topic[1].text.replace("_"," ")
			locdict2[loc_name]=lineData2		

	################### Calculating image Vectors####################
	givendictLoc={}
	locdict={}
	imageVectorList=[]
	vectorLen=len(givenObj["imageList"][0]["imgVectors"])
	for i in range(len(givenObj["imageList"])):
		given_imgList=[float(k) for k in givenObj["imageList"][i]["imgVectors"]]
		givenObj["imageList"][i]["imgVectors"]=given_imgList
	for m in range(vectorLen):
		sumFeatures=0
		for i in range(len(givenObj["imageList"])):
			sumFeatures+=givenObj["imageList"][i]["imgVectors"][m]
		imageVectorList.append(sumFeatures/len(givenObj["imageList"]))
	givendictLoc[loc_id]=imageVectorList

	############### Calculating location pair similarity################
	for key, images in locdict2.items():
		imageVectorList=[]
		for i in range(len(images)):
			new_imgList=[float(k) for k in images[i]["imgVectors"]]
			images[i]["imgVectors"]=new_imgList
		for m in range(vectorLen):
			sumFeatures=0
			for i in range(len(images)):
				sumFeatures+=images[i]["imgVectors"][m]
			imageVectorList.append(sumFeatures/len(images))
		locdict[key]=imageVectorList

	for key, locs in locdict.items():
		similarityScore1=euclidean_distance(locs,givendictLoc[loc_id])
		listPerUser1.append({"ID": key, "Score" :similarityScore1, "Images": ""})
						
	userlist1 = sorted(listPerUser1, key=lambda k: k['Score'], reverse=False)
	images=[]
	i=0
	########### Calculating similar image pairs#################
	while(i<int(k)):
		images=locdict2[userlist1[i]["ID"]]
		finImageDict={}
		similarImagePairs=[]
		for j in range(len(images)):
			new_imgList=[float(k) for k in images[j]["imgVectors"]]
			for m in range(len(givenObj["imageList"])):
				similarityScore2=L1_distance(new_imgList,givenObj["imageList"][m]["imgVectors"])
				similarImagePairs.append({"imagePairs":givenObj["imageList"][m]["imgID"] + " "+ images[j]["imgID"],"similarityScore":similarityScore2})
			
		userlist1[i]["Images"]=sorted(similarImagePairs, key=lambda k: k['similarityScore'], reverse=False)[:3]
		i=i+1
	

	print("********************L2 distance*****************\n")
	i=0
	while i < int(k):
		print(userlist1[i])
		i=i+1

# 
main()

