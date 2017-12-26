from data import Data as Data
from operator import itemgetter
from random import randint
from copy import deepcopy
import math

def jarakkmeans(centroidlama, centroidbaru):
	total = 0
	for x in range(0,len(centroidlama)-1):
		total += (float(centroidlama[x]) - float(centroidbaru[x]))**2

	return math.sqrt(total)

def createdbjarak(datajarak, datasetlist):
	for x in range(len(datasetlist) - 1):
		datajarak.append([])

	for x in range(len(datasetlist)):
		for y in range(x + 1, len(datasetlist)):
			datajarak[x].append(datasetlist[x].jarak(datasetlist[y]))


def getjarak(datajarak, indexc1, indexc2):
	if indexc1 > indexc2:
		x = indexc2
		y = indexc1
	else:
		x = indexc1
		y = indexc2

	return datajarak[x][y - x - 1]


def singlelinkage(cluster1, cluster2, datajarak, idclust1, idclust2):
	jarak = []
	for x in range(len(cluster1)):
		for y in range(len(cluster2)):
			jarak.append(
				[idclust1, idclust2, getjarak(datajarak=datajarak, indexc1=cluster1[x][0], indexc2=cluster2[y][0])])

	jarak.sort(key=itemgetter(2))
	return jarak[0]


def completelinkage(cluster1, cluster2, datajarak, idclust1, idclust2):
	jarak = []
	for x in range(len(cluster1)):
		for y in range(len(cluster2)):
			jarak.append(
				[idclust1, idclust2, getjarak(datajarak=datajarak, indexc1=cluster1[x][0], indexc2=cluster2[y][0])])

	jarak.sort(key=itemgetter(2), reverse=True)
	return jarak[0]


def averagelinkage(cluster1, cluster2, datajarak, idclust1, idclust2):
	jarak = 0
	for x in range(len(cluster1)):
		for y in range(len(cluster2)):
			jarak += getjarak(datajarak=datajarak, indexc1=cluster1[x][0], indexc2=cluster2[y][0])

	return [idclust1, idclust2, jarak / (len(cluster1) + len(cluster2))]


def meankor(cluster, panjangdimensi):
	centroidtmp = []
	for x in range(panjangdimensi):
		totaltmp = 0
		for y in range(len(cluster)):
			totaltmp += cluster[y][1].data[x]
		if len(cluster) > 0:
			centroidtmp.append(totaltmp / len(cluster))
		else:
			centroidtmp.append(0)
	return centroidtmp


def centroidlinkage(cluster1, cluster2, datajarak, idclust1, idclust2, panjangdimensi):
	korclust1 = meankor(cluster=cluster1, panjangdimensi=panjangdimensi)
	korclust2 = meankor(cluster=cluster2, panjangdimensi=panjangdimensi)

	return [idclust1, idclust2, jarakkmeans(centroidlama=korclust1, centroidbaru=korclust2)]


def linkage(datasetlist, jumlahcluster, panjangdimensi, metodepenghitunganjarak):
	datasetlisttmp = deepcopy(datasetlist)
	cluster = []

	datajarak = []

	createdbjarak(datajarak=datajarak, datasetlist=datasetlist)

	for x in range(len(datasetlisttmp)):
		cluster.append([[x, datasetlisttmp[x]]])

	i = 0
	while len(cluster) != jumlahcluster:
		jarak = []
		for x in range(len(cluster)):
			for y in range(x + 1, len(cluster)):
				if metodepenghitunganjarak == 1:
					jarak.append(
						singlelinkage(cluster1=cluster[x], cluster2=cluster[y], datajarak=datajarak, idclust1=x,
									  idclust2=y))
				elif metodepenghitunganjarak == 2:
					jarak.append(
						centroidlinkage(cluster1=cluster[x], cluster2=cluster[y], datajarak=datajarak, idclust1=x,
										idclust2=y, panjangdimensi=panjangdimensi))
				elif metodepenghitunganjarak == 3:
					jarak.append(
						completelinkage(cluster1=cluster[x], cluster2=cluster[y], datajarak=datajarak, idclust1=x,
										idclust2=y))
				elif metodepenghitunganjarak == 4:
					jarak.append(
						averagelinkage(cluster1=cluster[x], cluster2=cluster[y], datajarak=datajarak, idclust1=x,
									   idclust2=y))

		jarak.sort(key=itemgetter(2))
		print(jarak[0])
		print(jarak[1])
		print(jarak[2])

		for x in range(len(cluster[jarak[0][1]])):
			cluster[jarak[0][0]].append(cluster[jarak[0][1]][x])
		del cluster[jarak[0][1]]

		print(len(cluster))

	f = open('output.txt', 'w')
	for x in range(len(cluster)):
		for y in range(len(cluster[x])):
			f.write(str(cluster[x][y][1].index)+','+str(x))
			f.write('\n')
			print str(cluster[x][y][1].index)+','+str(x)
	f.close()


	# for x in range(len(cluster)):
	# 	print("Jumlah data pada cluster ke " + str(x + 1) + " = " + str(len(cluster[x])))
