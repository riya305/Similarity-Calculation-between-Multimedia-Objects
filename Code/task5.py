
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
	givenObj={}
	userlist1=[]
	userlist2=[]
	locdict2={}
	modelObj={}

	loc_id = sys.argv[1]
	k = sys.argv[2]
	flag=0
	userID=""
	doc = etree.parse("/home/riya/Code/devset_topics.xml")
	modelList=("CM", "CM3x3", "CN", "CN3x3","CSD","GLRLM", "GLRLM3x3","HOG","LBP", "LBP3x3")
	topicElem = doc.getroot()
	for topic in topicElem:
		if(loc_id==topic[0].text):
			for i in range(len(modelList)):
				with open('/home/riya/Code/descvis/img/'+topic[1].text+' '+modelList[i]+'.csv', 'rt') as f:
					reader = csv.reader(f, delimiter = ',', skipinitialspace=True)
					lineData = list()
					cols = next(reader)
					for line in reader:
						if line != []:
							# imagedict[line[0]]=line[1:]
							lineData.append({"imgID":line[0],"imgVectors":line[1:]})
				loc_name = topic[1].text.replace("_"," ")
				givenObj[modelList[i]]={"loc_name":loc_name,"imageList":lineData,"vectorLen":len(lineData[0]["imgVectors"])}
		else:
			loc_name = topic[1].text.replace("_"," ")
			for i in range(len(modelList)):
				modelLocList=[]
				with open('/home/riya/Code/descvis/img/'+topic[1].text+' '+modelList[i]+'.csv', 'rt') as f:
					reader = csv.reader(f, delimiter = ',', skipinitialspace=True)
					lineData2 = list()
					cols = next(reader)
					for line in reader:
						if line != []:
							lineData2.append({"imgID":line[0],"imgVectors":line[1:]})
				modelLocList.append({"vectorLen":len(lineData2[0]["imgVectors"]),"data":lineData2,"Model":modelList[i]})
			modelObj[loc_name]=modelLocList		

# 
	# for j in range(len(givenObj["imageList"])):
	# print(len(givenObj["imageList"]))
	# # dict1 = union2(elemdict[lineData[0][0]],giventermdict)
	# # dict2 = union2(giventermdict,elemdict[lineData[0][0]])
	# print(givenObj["imageList"][0]["imgVectors"])
	# # print("\n\n")
	
	locdict={}
	Locationdict={}
	modeldict={}
	givenLocDict={}
	givenModelDict={}
	givenLocModelAvgDict={}
	locModelAvgDict={}
	for j in range(len(modelList)):
		imageVectorList=[]
		for i in range(len(givenObj[modelList[j]]["imageList"])):
			given_imgList=[float(k) for k in givenObj[modelList[j]]["imageList"][i]["imgVectors"]]
			givenObj[modelList[j]]["imageList"][i]["imgVectors"]=given_imgList
		for i in range(len(givenObj[modelList[j]]["imageList"])):
			for m in range(len(givenObj[modelList[j]]["imageList"][i]["imgVectors"])):
				numMinMax=givenObj[modelList[j]]["imageList"][i]["imgVectors"][m]-min(givenObj[modelList[j]]["imageList"][i]["imgVectors"])
				denMinMax=max(givenObj[modelList[j]]["imageList"][i]["imgVectors"])-min(givenObj[modelList[j]]["imageList"][i]["imgVectors"])
			imageVectorList.append(numMinMax/denMinMax)	
		givenLocDict[loc_id]={"locVector":imageVectorList,"modelName":modelList[j]}
		givenModelDict[modelList[j]]={"locVector":imageVectorList,"locName":loc_id}

	
	# print(givenLocDict)
	modelSumList=[]	
	for key, locations in modelObj.items():
		modelList1=[]
		for j in range(len(locations)):
			images=locations[j]
			imageVectorList=[]
			modelSumList=[]	
			sumVectors=0
			for i in range(len(images["data"])):
				new_imgList=[float(k) for k in images["data"][i]["imgVectors"]]
				images["data"][i]["imgVectors"]=new_imgList		
			for i in range(len(images["data"])):
				for m in range(len(images["data"][i]["imgVectors"])):
					sumVectors+=images["data"][i]["imgVectors"][m]
					numMinMax=images["data"][i]["imgVectors"][m]-min(images["data"][i]["imgVectors"])
					denMinMax=max(images["data"][i]["imgVectors"])-min(images["data"][i]["imgVectors"])
				imageVectorList.append(numMinMax/denMinMax)
				modelSumList.append(sumVectors)
			modelList1.append({"modelName":locations[j]["Model"],"locVector":imageVectorList,"locName":key,"modelSumList":modelSumList})
		Locationdict[key]={"locVector":imageVectorList,"modelList":modelList1}
			
	# print(modeldict)
	contribution=[]
	for models,locs in Locationdict.items():
		for i in range(len(locs["modelList"])):
			locModelAvgDict[locs["modelList"][i]["locName"]]=sum(locs["modelList"][i]["locVector"])/len(locs["modelList"][i]["locVector"])

	for models,loc in givenModelDict.items():
		givenLocModelAvgDict[loc["locName"]]=sum(loc["locVector"])/len(loc["locVector"])


	
	# print(locModelAvgDict)
	similarityList=[]
	
	for givenLoc, givenValue in givenLocModelAvgDict.items():
		for loc, value in locModelAvgDict.items():
			similarityScore=[]
			for j in range(len(modelList)):
				similarityScore.append({"Model":modelList[j],"Contribution":modelSumList[j]/(value)})
			similarityList.append({"Location Name":loc,"Score":abs(givenValue-value),"Model":similarityScore})



	userlist1 = sorted(similarityList, key=lambda k: k['Score'], reverse=False)


	print("********************L1 distance*****************\n")
	i=0
	while i < int(k):
		print(userlist1[i])
		print("\n")
		i=i+1
# 
main()


