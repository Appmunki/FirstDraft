import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import random as rnd

class ContourFinder:
    def __init__(self):
#        Logger._level = Logger.DEBUG
#        self.marginoferrorweight =7
        pass
    @classmethod
    def findContours(self,edg):
        #plt.imshow(edg)
        #plt.show()
        temp = []
        cont = []
        contours, hir = cv2.findContours(edg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        Z = zip(contours,hir[0])
        noneable = lambda x: x == None
        for i,z in enumerate(Z) :
            if(noneable(z[0])):
                continue
            c = z[0]
            b = cv2.boundingRect(c)
            if cv2.contourArea(c)>500:  
                x,y,w,h = cv2.boundingRect(c)
                for i2,z2 in enumerate(Z[i+1:]): 
                    if(noneable(z2[0])):
                        continue
                    ri2 = i+1+i2
                    c2 = z2[0]
                    x2,y2,w2,h2 = cv2.boundingRect(c2)
                    if(abs(x-x2)<7 and abs(y2-y)<7 and abs(h-h2)<7 and abs(w-w2)<7):
                        Z[ri2] = (None,z2[1][3])
            else:
                Z[i]=(None,z[1][3])         
        trueHeir = {}
        if 1:
            for i,z in enumerate(Z):
                if(noneable(z[0])):
                    continue
                parent = z[1][3]
                if parent < 0:
                    continue
                #print parent, Z[parent]
                count = 0
                while(parent >= 1 and noneable(Z[parent][0])):
                    #print parent, Z[parent]
                    parent = Z[parent][1]
                    count+=1
                    assert(count<10)
                if parent in trueHeir:
                    trueHeir[parent].append(i)
                else:
                    trueHeir[parent] = [i]
        
        return contours, trueHeir
    @classmethod
    def processImage( self, imgfile ) :
        src = cv2.imread(imgfile);
        
        
        finalimg = src.copy()
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) # convert to grayscale
        edges = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        cont = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        #cv2.multiply(gray, 2, gray)    
        
        
        #    /---- doing threshold filtering ----
        #ray = cv2.GaussianBlur(gray, (5, 5), 0)
        
        #    \------finished with contours
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        gray=cv2.erode(gray,kernel)
        gray=cv2.dilate(gray,kernel)
        
        #    /---- canny edge filtering ----
        
        
        mix1 = cv2.add(gray, edges) #construct red channel
        mix2 = cv2.subtract(gray, edges) # constuct blue, green channel
        color = cv2.merge([mix2, mix2, mix1])
        #    \------finished canny
        
        
        
        #    /---- debugs contours ----/
        contimg = finalimg.copy()
        contours, hir = self.findContours(gray)

        for i, c in enumerate(contours):
            linecolor  = (0,100, 100)
            cv2.drawContours(contimg, contours, i, linecolor, 3)
        
        
        #crops the image and fills croppedImage array
        croppedImages = []
        cutoutimg = finalimg.copy()
        for i, cnt in enumerate(contours):
        
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)   
            # mask (of course replace corners with yours)
            mask = np.zeros(cutoutimg.shape, dtype=np.uint8)
            white = (255, 255, 255)
            cv2.fillConvexPoly(mask, approx, white)
            
            # apply the mask
            masked_image = cv2.bitwise_and(cutoutimg, mask)
            x,y,w,h = cv2.boundingRect(cnt)
            crop = masked_image[y+7:y+30,max(x+w-35,0):x+w-7]
            #crop = masked_image[y:y+h,x:x+w]
            croppedImages.append(crop)
        del hir[0]
        return contours[1:], hir, croppedImages[1:]
   

class ContourNode:
    def __init__(self, contour, img):
        x,y,w,h = cv2.boundingRect(contour)
        self.bbox = (x,y,w,h)
        self.img = img
        self.children = []
    def addChild(self, cnode):
        self.children.append(cnode)

def dictParse(contourArray, croppedImages, indicesDict, index):
    print len(contourArray)
    thisnode = ContourNode(contourArray[index-1],croppedImages[index-1])
    if(indicesDict.has_key(index)):
        for childNode in indicesDict[index]:
            thisnode.addChild(dictParse(contourArray, croppedImages, indicesDict, childNode))
    return thisnode
