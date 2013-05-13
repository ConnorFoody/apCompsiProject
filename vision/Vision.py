# Basic circle detection using OpenCV
import math
import sys
    
import cv2
#import cv2.cv as cv
import numpy as np

class CircleFind(object):
    
    targetColor = (0, 0, 255)
    missedColor = (0, 255,0)
    
    # constants that need to be tuned
    kHoleClosingIterations = 9
    def __init__(self):
        self.morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3), anchor=(1,1))
        self.size = None
    
    def processImage(self, img):
        heading = 0
        
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            self.bin = np.empty((h, w, 1), dtype=np.uint8)
        temp = img
        targets = []
        HIGH = 80
        LOW = 10
        cv2.blur(img, (7,7), dst=img)
        img = cv2.Canny(img, LOW, HIGH)
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        #return img
        circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 10, param1=HIGH,param2=5,minRadius=1,maxRadius=500)
        if(circles == None):
            print "O nose!!!, nothing in circles!"
            return img
        print circles[0][0][0]
        x = circles[0][0][0]
        y = circles[0][0][1]
        radius = circles[0][0][2]
        cv2.circle(cimg, (x,y), 7, self.targetColor, thickness=radius)
        return cimg
 
if __name__ == '__main__':
    
    prg = CircleFind()
    tmp = cv2.imread("images/img5.jpg")
    img = tmp
    img = prg.processImage(img)
    cv2.imshow('Processed', img)
    
    print "Hit ESC to exit"
    
    while True:
        key = 0xff & cv2.waitKey(1)
        if key == 27:
            break

