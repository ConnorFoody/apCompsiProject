# Basic circle detection using OpenCV
import math
import sys

import cv2
import numpy as np


class CircleFind(object):
    
    targetColor = (255, 0, 0)
    missedColor = (255,255,0)
    
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
            self.rbg = np.empty((h, w, 1), dtype=np.uint8)
            self.r = np.empty((h, w, 1), dtype=np.uint8)
            self.g = np.empty((h, w, 1), dtype=np.uint8)
            self.b = np.empty((h, w, 1), dtype=np.uint8)
            self.ri = np.empty((h, w, 1), dtype=np.uint8)
            self.gi = np.empty((h, w, 1), dtype=np.uint8)
            self.bi = np.empty((h, w, 1), dtype=np.uint8)
        # convert to HSV
        cv2.split(img, [self.r, self.g, self.b])
        cv2.split(img, [self.ri, self.gi, self.bi])
    
        # uncommment this to draw on zeroed image
        #img = np.zeros(img.shape, dtype=np.uint8)
        
        # Threshold each component separately
        # Hue
        # NOTE: Red is at the end of the color space, so you need to OR together
        # a thresh and inverted thresh in order to get points that are red
        #cv2.threshold(self.hue, 60-15, 255, type=cv2.THRESH_BINARY, dst=self.bin)
        #cv2.threshold(self.hue, 60+15, 255, type=cv2.THRESH_BINARY_INV, dst=self.hue)
        #cv2.threshold(self.hue, 60-15, 255, type=cv2.THRESH_BINARY, dst=self.bin)
        cv2.threshold(self.bi, 150, 255, type=cv2.THRESH_BINARY_INV, dst=self.bi)
        cv2.threshold(self.b, 135, 255, type=cv2.THRESH_BINARY, dst=self.b)

        cv2.threshold(self.gi, 150, 255, type=cv2.THRESH_BINARY_INV, dst=self.gi)
        cv2.threshold(self.g, 100, 255, type=cv2.THRESH_BINARY, dst=self.g)

        cv2.threshold(self.ri, 150, 255, type=cv2.THRESH_BINARY_INV, dst=self.ri)
        cv2.threshold(self.r, 60, 255, type=cv2.THRESH_BINARY, dst=self.r)

        cv2.bitwise_and(self.ri, self.r, dst=self.r)
        cv2.bitwise_and(self.gi, self.g, dst=self.g)
        cv2.bitwise_and(self.bi, self.b, dst=self.b)
        # Combine the results to obtain our binary image which should for the most
        # part only contain pixels that we care about
        cv2.bitwise_and(self.r, self.g, dst=self.bin)
        cv2.bitwise_and(self.bin, self.b, dst=self.bin)
        
        # Uncommment this to show the thresholded image
        #cv2.imshow('bin', self.bin)
        
        # Fill in any gaps using binary morphology
        cv2.morphologyEx(self.bin, cv2.MORPH_CLOSE, self.morphKernel, dst=self.bin, iterations=self.kHoleClosingIterations)
        return self.bin
        # Find contours
        contours = self.findConvexContours(self.bin)
        targets = []
        for c in contours:
            (x,y), radius = cv2.minEnclosingCircle(c)
            targets.append((int(x),int(y)))
            cv2.circle(img, (int(x),int(y)) ,7, self.targetColor)
            print (x,y)
        if(len(targets) == 0):
            print "o nose! nothing found"
            return self.bin
        
        cv2.circle(img, targets[0] ,7, self.targetColor)
        cv2.drawContours(img, contours, -1, self.missedColor, thickness = 3)
        return img
        
        
    def boundAngle0to360Degrees(self, angle):
        # Naive algorithm
        while (angle >= 360.0):
            angle -= 360.0
            
        while (angle < 0.0):
            angle += 360.0
            
        return angle
    
    def findConvexContours(self, img): 
        img = img.copy()
        
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
        return [cv2.convexHull(c, clockwise=True, returnPoints=True) for c in contours]
    

if __name__ == '__main__':
    
    prg = CircleFind()
    tmp = cv2.imread("images/img5.jpg")
    img = tmp
    img = prg.processImage(img)
    cv2.imshow('Processed', img)
    #cv2.imshow('Original', tmp)
    
    print "Hit ESC to exit"
    
    while True:
        key = 0xff & cv2.waitKey(1)
        if key == 27:
            break

