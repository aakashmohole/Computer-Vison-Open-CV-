import cv2
import numpy as np 

img = cv2.imread('D:\\OpenCV\\Images\\hand.jpg')
img = cv2.resize(img,(400,500))
img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# blure for bettr res
blured = cv2.medianBlur(img1,11)
# threshold
ret,thres = cv2.threshold(blured,240,255,cv2.THRESH_BINARY)
dilata = cv2.dilate(thres,(1,1),iterations = 6)

#findcontour(img,contour_retrival_mode,method)
# now draw contrours
cnts,hier = cv2.findContours(thres,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#Here cnts is a list of contours. ANd each contour is an array with x, y cordinate   
#hier variable called hierarchy and it contain image information.
print("Number of contour==",cnts,"\ntotal contour==",len(cnts))
print("Hierarchy==\n",hier)

for c in cnts:
    epsilon = 0.0001 * cv2.arcLength(c,True) 
    data = cv2.approxPolyDP(c,epsilon,True)  
    
    hull = cv2.convexHull(data)

    cv2.drawContours(img,[c],-1, (50, 50, 150), 2)
    cv2.drawContours(img,[hull],-1, (50, 50, 150), 2)

    
#find convexity defect
hull2 = cv2.convexHull(cnts[0],returnPoints = False)
#defect returns an array which contain value  [start_point, end_point, farthest_point, approximate_distance to farthest point ]
defect = cv2.convexityDefects(cnts[0],hull2)

for i in range(defect.shape[0]):
    s,e,f,d = defect[i,0]
    print(s,e,f,d)
    start = tuple(c[s][0])
    end = tuple(c[e][0])
    far = tuple(c[f][0])
    #cv2.line(img,start,end,[255,0,0],2)
    cv2.circle(img,far,5,[0,0,255],-1)
    

  
#Extreme Points----
#It means topmost, bottommost, rightmost and leftmost points of the object.

c_max = max(cnts, key=cv2.contourArea)

# determine the most extreme points along the contour
extLeft = tuple(c_max[c_max[:, :, 0].argmin()][0])
extRight = tuple(c_max[c_max[:, :, 0].argmax()][0])
extTop = tuple(c_max[c_max[:, :, 1].argmin()][0])
extBot = tuple(c_max[c_max[:, :, 1].argmax()][0])

# draw the outline of the object, then draw each of the
# extreme points, where the left-most is red, right-most
# is green, top-most is blue, and bottom-most is teal

cv2.circle(img, extLeft, 8, (255, 0, 255), -1)  #pink
cv2.circle(img, extRight, 8, (0, 125, 255), -1) #brown
cv2.circle(img, extTop, 8, (255, 10, 0), -1)  #blue
cv2.circle(img, extBot, 8, (19, 152, 152), -1) #green

cv2.imshow('orignal',img)
cv2.imshow('gray',img1)
cv2.imshow('thresh',thres)

cv2.waitKey(0)
cv2.destroyAllWindows()