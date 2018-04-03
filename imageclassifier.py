from PIL import Image
import csv
import os
import sys
import matplotlib.pyplot as plt
import random
import operator

sys.setrecursionlimit(2000)
#-------------Global Declarations---------------
oldCluster1 = []
oldCluster2 = []
firstPass = 0
countForAccuracy = 0
countTotalForACcuracy = 0
localCheck = 0
d = []
fp = 0 
nc =[]
singlCluster = []
cnt = 1
#------------------------------------------------


#-------------For training the dataset, creating a lookup table by name, lookup.csv------------------
def train (folder1,folder2,folder3):
	f = open('lookup.csv' , 'wb')
	i = 1
	if folder3 == 'NULLFOLDER':
		limitOfi = 2
	else: limitOfi = 3 
	while i <= limitOfi:
		if i == 1: folder = folder1
		elif i == 2 : folder = folder2
		elif i == 3 : folder = folder3 
		for filename in os.listdir(folder):
			if filename.endswith(".jpeg"):
				label = ''
				if filename[0] == 'h':
					label = 'headshot'
				elif filename[0] == 'l':
					label = 'landscape'
				im = Image.open(folder+filename)
				hist = histogram(im)
				writeToCSV(f,filename,label,hist)

			else :
				print "No image found"
		i = i+1
	f.close()
#------------------------------------------------------------------------------------

#--------------------------------validating a dataset, in 3 fold crossvalidation------------------------
def validate (folder):
	kcounter = 1
	sumOfAccuracy = 0
	while kcounter <= 10:
		count = 0
		countTotal = 0
		print '--------For k = %i -------'%(kcounter)
		for filename in os.listdir(folder):
			if filename.endswith(".jpeg"):
				label1 = ''
				label = ''
				if filename[0] == 'h':
					label = 'headshot'
				elif filename[0] == 'l':
					label = 'landscape'
				boolval = 'False'
				im = Image.open(folder+filename)
				hist = histogram(im)
				dist = []
				g = open('lookup.csv' , 'r')
				reader = csv.reader(g)
				for row in reader:
					array = [float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])]
					dist.append((manhattandistance(array,hist),row[0],row[1]))
				dist = sorted(dist)
				g.close()
				i = 0
				nearestNeighbours = []
				while (i < kcounter):
					nearestNeighbours.append(dist[i])
					i = i+1
				headshotCount = 0
				landscapeCount = 0
				for elem in nearestNeighbours:
					if elem [2] == 'headshot':
						headshotCount = headshotCount + 1
					if elem [2] == 'landscape':
						landscapeCount = landscapeCount + 1
				if headshotCount > landscapeCount:
					label1 = 'headshot'
				elif landscapeCount > headshotCount:
					label1 = 'landscape'
				elif headshotCount == landscapeCount:
					label1 = 'Both'
				
				if label == label1:
					boolval = 'True'
					count = count + 1
				print filename + '\t' + label + ' ' + '::' + ' ' + label1 + '\t' + boolval
				countTotal = countTotal + 1
		accuracy = (float(count) / countTotal)*100
		sumOfAccuracy = sumOfAccuracy + accuracy
		print 'Accuracy : ' + str(accuracy)
		kcounter = kcounter + 1
	return sumOfAccuracy
#-------------------------------------------------------------------------------------------------

#-------------------------------------KNN for users single image-------------------------------------
def knnForSinlgeImage (filename,k):
	g = open('lookup.csv' , 'r')
	reader = csv.reader(g)
	label1 = ''
	boolval = 'False'
	if filename.endswith(".jpeg"):
		im = Image.open(filename)
		hist = histogram(im)
		dist = []
		for row in reader:
			array = [float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])]
			dist.append((manhattandistance(array,hist),row[0],row[1]))
		dist = sorted(dist)
		i = 0
		nearestNeighbours = []
		while (i < k):
			nearestNeighbours.append(dist[i])
			i = i+1
		headshotCount = 0
		landscapeCount = 0
		for elem in nearestNeighbours:
			if elem [2] == 'headshot':
				headshotCount = headshotCount + 1
			if elem [2] == 'landscape':
				landscapeCount = landscapeCount + 1
		if headshotCount > landscapeCount:
			label1 = 'headshot'
		elif landscapeCount > headshotCount:
			label1 = 'landscape'
		elif headshotCount == landscapeCount:
			label1 = 'Both'
		print filename + ' ' + '::' + ' ' + label1
	else: print 'No image found' 
	g.close() 
#-----------------------------------------------------------------------------------------------------------

#--------------------------------------Computation of histogram for an image----------------------------------
# The logic for how to compute a histogram without using the direct function was give by Prof. Natalia Khuri--------------
def histogram (im):
	rawdata = list(im.getdata())
	sumr1,sumr2,sumg1,sumg2,sumb1,sumb2 = 1,1,1,1,1,1
	lenOfRawData = len(rawdata)
	for pixel in rawdata:
		if pixel[0] >=0 and pixel[0] <= 127:
			sumr1 = sumr1+1
		if pixel[0] > 127 and pixel[0] <= 255:
			sumr2 = sumr2 + 1
		if pixel[1] >=0 and pixel[1] <= 127:
			sumb1 = sumb1 + 1
		if pixel[1] > 127 and pixel[1] <= 255:
			sumg1 = sumg1 + 1
		if pixel[2] >=0 and pixel[2] <= 127:
			sumb1 = sumb1 + 1
		if pixel[2] > 127 and pixel [2] <= 255:
			sumb2 = sumb2 + 1
	avgR1 = float (sumr1) / lenOfRawData
	avgR2 = float (sumr2) / lenOfRawData
	avgG1 = float (sumg1) / lenOfRawData
	avgG2 = float (sumg2) / lenOfRawData
	avgB1 = float (sumb1) / lenOfRawData
	avgB2 = float (sumb2) / lenOfRawData
	return [avgR1,avgR2,avgG1,avgG2,avgB1,avgB2]
#--------------------------------------------------------------------------------------------------------------

#-------------------------------write the histogram and related data to image to a CSV file---------------------
def writeToCSV (f,filename,label,hist):
	writer = csv.writer(f)
	row = [filename,label]+hist
	writer.writerow(row)	
#-----------------------------------------------------------------------------------------------------------------


#---------------------------Compute manhattan distance using histogram between two images----------------------
def manhattandistance(array,hist):
	sum = 0
	i = 0
	while i < len(array):
		sum = sum + abs(array[i] - hist[i])
		i = i+1
	return sum
#-------------------------------------------------------------------------------------------------------------

#-----------------------Plot the graph for 3 fold cross validation-------------------------------------------
def drawgraph(fold,fold1):
	plt.plot([fold],[fold1],'s')
#----------------------------------------------------------------------------------------------------------

#-----------------------------------Kmeans for clustering computation-------------------------------------------
def kmeansComputation(histForC1,histForC2):
	global oldCluster1,oldCluster2,firstPass,countForAccuracy,countTotalForACcuracy
	newCluster1 = []
	newCluster2 = []
	g = open('lookup.csv' , 'rb')
	reader = csv.reader(g)
	for row in reader:
		histOfThisRow = [float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])]
		d1 = manhattandistance(histOfThisRow,histForC1)
		d2 = manhattandistance(histOfThisRow,histForC2)
		if d1 < d2:
			newCluster1.append(row)
		if d2 < d1:
			newCluster2.append(row)
		if d1 == d2:
			newCluster1.append(row)
			newCluster2.append(row)

	if firstPass == 0:
		oldCluster1 = newCluster1
		oldCluster2 = newCluster2
		histForC1 = mean(newCluster1)
		histForC2 = mean(newCluster2)
		firstPass = 1
		kmeansComputation(histForC1,histForC2)
	elif firstPass == 1:	
		if oldCluster1 != newCluster1 and oldCluster2 != newCluster2:
			oldCluster2 = newCluster2
			oldCluster1 = newCluster1
			histForC1 = mean(newCluster1)
			histForC2 = mean(newCluster2)
			kmeansComputation(histForC1,histForC2)
		elif oldCluster1 == newCluster1 and oldCluster2 == newCluster2:
			print '\n----------------Landscape Cluster------------------\n' 
			for elem in newCluster1:
				print elem[0] +'::' + elem[1]
				countTotalForACcuracy = countTotalForACcuracy + 1
				if elem[1] == 'landscape':
					countForAccuracy = countForAccuracy + 1
			print '\n------------------Headshot Cluster-------------------------\n'
			for elem in newCluster2:
				print elem[0] + '::' + elem[1]
				countTotalForACcuracy = countTotalForACcuracy + 1
				if elem[1] == 'headshot':
					countForAccuracy = countForAccuracy + 1
			print 'Accuracy of kmeans clustering is: ' + str((float(countForAccuracy) / countTotalForACcuracy)*100) + '%\n'
			menu()
#--------------------------------------------------------------------------------------------------------------

#-----------------------------used by kmeans to compute the new cluster using mean of histogram-----------------------
def mean(newCluster):
	meanr1 = 0
	meanr2 = 0
	meang1 = 0
	meang2 = 0
	meanb1 = 0
	meanb2 = 0
	
	for elem in newCluster:
		meanr1 = meanr1 + float(elem[2])
		meanr2 = meanr2 + float(elem[3])
		meang1 = meang1 + float(elem[4])
		meang2 = meang2 + float(elem[5])
		meanb1 = meanb1 + float(elem[6])
		meanb2 = meanb2 + float(elem[7])
	meanr1 = meanr1 / len(newCluster)
	meanr2 = meanr2 / len(newCluster)
	meang1 = meang1 / len(newCluster)
	meang2 = meang2 / len(newCluster)
	meanb1 = meanb1 / len(newCluster)
	meanb2 = meanb2 / len(newCluster)
	return [meanr1,meanr2,meang1,meang2,meanb1,meanb2]
#---------------------------------------------------------------------------------------------------------------------

#----------------------------- Kmeans first pass-----------------------------------------------------------
def kmeans():
	global countForAccuracy,countTotalForACcuracy,firstPass
	countForAccuracy = 0
	countTotalForACcuracy=0
	firstPass = 0
	r = random.randint(1,60)
	c1 = 'l'+str(r)+'.jpeg'
	c2 = 'h'+str(r)+'.jpeg'
	histForC1 = []
	histForC2 = []
	g = open('lookup.csv' , 'rb')
	reader = csv.reader(g)
	for row in reader:
		if row[0] == c1:
			histForC1 = [float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])]
		if row[0] == c2:
			histForC2 = [float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])]
	g.close()
	kmeansComputation(histForC1,histForC2)	
#----------------------------------------------------------------------------------------------------

#-----------------------------------Single linkage---------------------------------------------------------
def singleLinkage():
	global d
	global fp
	global nc
	global singlCluster
	global cnt
	extractCSV = []
	x=0
	y=0
	yarray=[]
	minim = []
	tempD = []
	finalmin = 0
	if fp == 0:
		g = open('lookup.csv' , 'rb')
		reader = csv.reader(g)
		for row in reader:
			extractCSV.append(row)
		for row in extractCSV:
			histOfThisRow = [float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])]
			d1=[]
			for row1 in extractCSV:
				if row[0] != row1[0]:
					histOfThisRow1 = [float(row1[2]),float(row1[3]),float(row1[4]),float(row1[5]),float(row1[6]),float(row1[7])]
					d1.append(manhattandistance(histOfThisRow,histOfThisRow1))
				if row[0] == row1[0]:
					d1.append('ZERO')

			minim.append(min(d1))
			yarray.append(d1.index(min(d1)))	
			d.append(d1)
		finalmin = min(minim)
		x = minim.index(min(minim))
		y = yarray[x]
		nc = [x,y]
		singlCluster.append([nc[:],finalmin])
		fp =1
		print cnt
		cnt = cnt+1
		singleLinkage()
	elif fp ==1:
		for row in d:
			i = 0
			colD = []
			while i < len(row):
				if (i not in nc) and (d.index(row) not in nc):
					colD.append(row[i])
				elif (i in nc) and (d.index(row) not in nc):
					colD.append(mini(d.index(row)))
				elif (i not in nc) and (d.index(row) in nc):
					colD.append(mini(i))
				elif (i in nc) and (d.index(row) in nc):
					if i == d.index(row):
						colD.append('ZERO')
					else:
						colD.append('C')
				i = i+1
			minim.append(min(colD))
			yarray.append(colD.index(min(colD)))
			tempD.append(colD)
		finalmin = min(minim)
		if cnt == 36:
			print tempD
			sys.exit()
		if finalmin == 'C':
			printSLCluster()
			sys.exit()
			#menu()
		x = minim.index(min(minim))
		y = yarray[x]
		if (x in nc) and (y not in nc):
			nc.append(y)
		elif (x not in nc) and (y in nc):
			nc.append(x)
		elif (x not in nc) and (y not in nc):
			nc = [x,y]
		singlCluster.append([nc[:],finalmin])
		print cnt
		cnt = cnt+1
		singleLinkage()
#-----------------------------------------------------------------------------------------------------------------		

#----------------------------used by single linkage to get the min distance while making clusters-----------------
def mini(ind):
	global nc
	a=[]
	for elem in nc:
		a.append(d[elem][ind])
	return min(a)
#---------------------------------------------------------------------------------------------------------------

#---------------------------prints the clusters from the distance matrix--------------------------------------
def printSLCluster():
	global singlCluster
	g = open('lookup.csv','rb')
	reader=csv.reader(g)
	extractCSV = []
	for row in reader:
		extractCSV.append(row)
	for row in singlCluster:
		printBlock = []
		for elem in row[0]:
			printBlock.append(extractCSV[elem][0])
		print str(printBlock) +' clusters at ' + str(row[1])
#------------------------------------------------------------------------------------------------------------------
		
#-----------------------------------------------Menu, to provide interface based exit--------------------------------
def menu():
	global localCheck
	print 'Menu'
	print '1: To run 3 fold cross validation \n2: To classify a single image of your choice\n3: To apply kmeans\n4: To apply singlelinkage\n5: To exit'
	choice = input('Enter your choice : ')
	if choice == 1:
		print '---------------Fold 1------------------'
		train('1/','2/','NULLFOLDER')
		fold1 = float(validate('3/')) / 10
		print fold1
		print '---------------Fold 2------------------'
		train('2/','3/','NULLFOLDER')
		fold2 = float(validate('1/')) / 10
		print fold2
		print '---------------Fold 3------------------'
		train('1/','3/','NULLFOLDER')
		fold3 = float(validate('2/')) / 10
		print fold3

		drawgraph(1,fold1)
		drawgraph(2,fold2)
		drawgraph(3,fold3)
		plt.xlabel('Folds')
		plt.ylabel('Accuracy for a fold in %') 
		plt.show()
		print "Close the image to proceed"
		menu()

	if (choice == 2 or choice == 3) and localCheck == 0 :
		localCheck = 1
		train('1/','2/','3/')

	if choice == 2:
		k = input('Enter the value of K : ')
		image = raw_input('Enter the image file along with path if not in same directory as this file or in sub directory of this directory : ')
		if image.endswith(".jpg"):
			print 'Please change the file extension to .jpeg'
			menu()
		knnForSinlgeImage(image,k)
		menu()

	if choice == 3:
		kmeans()

	if choice == 4:
		train('a/','b/','c/')
		singleLinkage()

	if choice == 5:
		sys.exit()
#-----------------------------------------------------------------------------------------------------------

#--------------------------------------Main exectuion function------------------------------------------------------
def main():
	menu()
	
if __name__ == '__main__':
	main()
#---------------------------------------------------------The end----------------------------------------------------
	



