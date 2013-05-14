# Basic circle detection using OpenCV
import math
import sys
import time
import cv2
import numpy as np


class CircleFind(object):
    
    targetColor = (0, 0, 255)
    missedColor = (255,255,0)
    
    # constants that need to be tuned
    kHoleClosingIterations = 11
    def __init__(self):
        self.morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3), anchor=(1,1))
        self.size = None
    
    def processImage(self, img):
        heading = 0
        
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            self.bin = np.empty((h, w, 1), dtype=np.uint8)
            self.tmp = np.empty((h, w, 1), dtype=np.uint8)
            self.hsv = np.empty((h, w, 3), dtype=np.uint8)
            self.hue = np.empty((h, w, 1), dtype=np.uint8)
            self.sat = np.empty((h, w, 1), dtype=np.uint8)
            self.val = np.empty((h, w, 1), dtype=np.uint8)
           
        # convert to HSV
        cv2.cvtColor(img, cv2.cv.CV_BGR2HSV, self.hsv)
        cv2.split(self.hsv, [self.hue, self.sat, self.val])
    
        # uncommment this to draw on zeroed image
        #img = np.zeros(img.shape, dtype=np.uint8)
        
        # Threshold each component separately
        # Hue
        cv2.threshold(self.hue, 20, 255, type=cv2.THRESH_BINARY, dst=self.hue)
        
        # Saturation
        cv2.threshold(self.sat, 65, 255, type=cv2.THRESH_BINARY_INV, dst=self.tmp)
        cv2.threshold(self.sat, 55, 255, type=cv2.THRESH_BINARY, dst=self.sat)
        
        # Value
        cv2.threshold(self.val, 150, 255, type=cv2.THRESH_BINARY_INV, dst=self.bin)
        cv2.threshold(self.val, 110, 255, type=cv2.THRESH_BINARY, dst=self.val)

        cv2.bitwise_and(self.val, self.bin, self.bin)
        cv2.bitwise_and(self.tmp, self.sat, self.sat)
        
        cv2.bitwise_and(self.bin, self.sat, self.bin)
        cv2.bitwise_and(self.bin, self.hue, self.bin)
        
        # Fill in any gaps using binary morphology
        cv2.morphologyEx(self.bin, cv2.MORPH_CLOSE, self.morphKernel, dst=self.bin, iterations=self.kHoleClosingIterations)
        
        # Find contours
        contours = self.findConvexContours(self.bin)
        targets = []
        for c in contours:
            if self.isCircle(c):
                center, radius = cv2.minEnclosingCircle(c)
                targets.append((center, radius))

        if(len(targets) == 0):
            print "o nose! nothing found"
            return self.bin
        
        for tar in targets:
            (x,y) = tar[0]
            cv2.circle(img, (int(x),int(y)) ,7, self.targetColor)

        return img

    def isCircle(self, contour):
        arc = .01 * cv2.arcLength(contour, True)
        tmp = cv2.approxPolyDP(contour, arc, True)        
        if len(tmp) > 6:
            return True
        return False

    def findConvexContours(self, img): 
        img = img.copy()
        
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
        return [cv2.convexHull(c, clockwise=True, returnPoints=True) for c in contours]
    

if __name__ == '__main__':
    
    prg = CircleFind()
    end_time = 0.0
    
    start_time = time.time()
    img = cv2.imread("images/img5.jpg")
    img = prg.processImage(img)
    end_time = time.time()
    print end_time - start_time
    
    cv2.imshow('Processed', img)
    
    print "Hit ESC to exit"
    
    while True:
        key = 0xff & cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()

            break
