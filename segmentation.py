# # Text Segmentation
# Assumptions
# * The image has a dark background below the paper
# * The writing is darker than the paper.
# * The image is 1:1 aspect ratio

import cv2 
import numpy as np
import sys
from utils import *
sys.setrecursionlimit(1000000)

# Read Image
img = cv2.resize(cv2.imread(sys.argv[1]), (600,600))

# Convert image to grayscale for processing 
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Paper Segmentation
hist = [0]*256
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        hist[img_g[i][j]]+=1
hist = np.array(hist)/sum(hist)

# Otsu's Thresholding for paper segmentation
thresh = Otsu(hist)
paper = (img_g>thresh)*1.0

# Clearing characters on the paper using closing followed by openning
paper = cv2.dilate(paper,np.ones((10,10)))
paper = cv2.erode(paper,np.ones((10,10)))
paper = cv2.erode(paper,np.ones((10,10)))
paper = cv2.dilate(paper,np.ones((10,10)))

# Text Segmentation
# Considering only the paper pixels for Otsu's thresholding of the text
paper_hist = [0]*256
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if(paper[i][j]>0.99):
            paper_hist[img_g[i][j]]+=1
paper_hist = np.array(paper_hist)/sum(paper_hist)

# Otsu's Thresholding to get Text Mask
thresh = Otsu(paper_hist)
text = paper*(((paper*img_g).astype('uint8') < thresh ) *1.0)

# Openning text with a (1,15) box kernel to join letters of a word 
textdash = cv2.dilate(text,np.ones((3,3)))
textdash = cv2.dilate(textdash,np.ones((1,15)))
textdash = cv2.erode(textdash,np.ones((1,15)))
text = ((text+textdash)>0.5)*1.0

# Bounding Box Prediction
# Using DFS to idetify connected components
for i in range(text.shape[0]):
    for j in range(text.shape[1]):
        if(text[i][j]>0.5):
            m = dfs(text, i, j, float('inf'), -1, float('inf'), -1)
            if (m[1]-m[0])*(m[3]-m[2]) > 200 and (m[1]-m[0])*(m[3]-m[2]) < 600*150:
                img = cv2.rectangle(img, (m[2],m[0]), (m[3],m[1]), (0,0,255), 2)
cv2.imshow('final', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
