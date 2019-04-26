import cv2
import sys
import numpy as np
import math
#== Parameters =======================================================================
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 200
minLineLength = 10
maxLineGap =100
#== Processing =======================================================================

#-- Read image -----------------------------------------------------------------------
img = cv2.imread('idscan_3.png')
resized_image = cv2.resize(img, (512, 512), interpolation = cv2.INTER_AREA)

original_image = resized_image.copy()
gray = cv2.cvtColor(resized_image,cv2.COLOR_BGR2GRAY)

#-- Edge detection -------------------------------------------------------------------
edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)

#--Hough Transform-----------------------------------------------------------------
linesnew = cv2.HoughLinesP(image=edges,rho=0.05,theta=np.pi/180, threshold=80,lines=np.array([]), minLineLength=minLineLength,maxLineGap=50)

if linesnew == None:
    print "No id card in the image"
    sys.exit()

houghpoints = []
for x1,y1,x2,y2 in linesnew[0]:
    x = (x1 + x2)/2
    y = (y1 + y2)/2
    houghpoints.append([x,y])
    cv2.line(resized_image,(x1,y1),(x2,y2),(0,255,0),2)

#cv2.imshow('edges', edges)
#cv2.imshow('cleared', cleared)
#cv2.imshow('hough', resized_image)

#--finding contours-----------------------------------------------------------------
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

x_min = []
y_min = []
x_max = []
y_max = []

for c in (contours):
    rect = cv2.boundingRect(c)
    if rect[0] > 30 and rect[1]>30 and (rect[2]+rect[0]) < (resized_image.shape[1]-30) and (rect[3]+rect[1]) < (resized_image.shape[0]-30) :
        if rect[2]> 100 or rect[3]>100:
            for hoghpoints in houghpoints:
                if rect[0] < hoghpoints[0] < (rect[0] + rect[2]) and rect[1] < hoghpoints[1] < (rect[1] + rect[3]):
                    x,y,w,h = rect
                    x_min.append(x)
                    y_min.append(y)
                    x_max.append(x+w)
                    y_max.append(y+h)

xmin_final = min(x_min)
ymin_final = min(y_min)
xmax_final = max(x_max)
ymax_final = max(y_max)

cv2.rectangle(original_image,(xmin_final,ymin_final),(xmax_final,ymax_final),(0,255,0),2)
cv2.imshow('idscan_1_output', original_image)
cv2.imwrite('idscan_1_output.png', original_image)
cv2.waitKey(0)

#--Detecting the orientation of the id card ---------------------------

orientation = []
distance = []

for x1,y1,x2,y2 in linesnew[0]:
    if (x2 - x1) > 0:
        orientation.append(float((y2-y1)/(x2-x1)))
        distance.append(math.hypot(x2 - x1, y2 - y1))

orientation_index = distance.index(max(distance))
print "Orientation of id card is: ", orientation[orientation_index]        
