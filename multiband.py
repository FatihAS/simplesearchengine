import cv2
import numpy as np
import json
from data import Data as Data
from clustering import linkage


datasetlist = []
arrImgName = ["multiband/gb1.jpg","multiband/gb2.jpg","multiband/gb3.jpg","multiband/gb4.jpg","multiband/gb5.jpg","multiband/gb7.jpg"]

arrimg = []

for z in range(0,len(arrImgName)):
    tmpimg = cv2.imread(arrImgName[z])
    tmpimg = cv2.cvtColor(tmpimg, cv2.COLOR_BGR2GRAY)

    itr = 0
    for x in range(0,len(tmpimg)):
        for y in range(0,len(tmpimg[x])):
            if z == 0:
                arrimg.append([tmpimg[x][y]])
                itr += 1
            else:
                arrimg[itr].append(tmpimg[x][y])
                itr+=1

for x in range(0,len(arrimg)):
    data = Data(data=arrimg[x],index=x)
    datasetlist.append(data)

linkage(datasetlist, 6, len(arrImgName), 2)