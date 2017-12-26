import cv2
import numpy as np
from operator import itemgetter

filename = "centroid"
height = 32
width = 32
rgbarr = [[230, 126, 34],[231, 76, 60],[149, 165, 166],[26, 188, 156],[52, 152, 219],[155, 89, 182],[52, 73, 94],[241, 196, 15]]
result_image = np.zeros((height,width,3), np.uint8)

f = open(filename+".txt", "r")

imageindexstring = f.read()
imagetmp = imageindexstring.split("\n")
imagearr = []
brokenarr = []

for x in range(0,len(imagetmp)):
    imagearr.append(imagetmp[x].split(","))
    try:
        imagearr[x][0] = int(imagearr[x][0])
    except:
        brokenarr.append(x)
        
brokenarr.sort(reverse=True)

for x in range(0,len(brokenarr)):
    del imagearr[brokenarr[x]]


imagearr.sort(key=itemgetter(0))

for x in range(0,len(imagearr)):
    imagearr[x][1] = rgbarr[int(imagearr[x][1])]

for x in range(0,len(imagearr)):
    result_image[int(x/width)][x % width] = imagearr[x][1]

cv2.imwrite(filename+'.jpg',result_image)