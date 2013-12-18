# Basic circle detection using OpenCV
import math
import sys
import time
import cv2
import numpy as np


#
#   Need to work on this soonish... here is plan: 
#       1) find outer most lines, top intersections
#       2) use the top intersections to establish regions of interest
#       3) hough the ROI to establish skew, proportionality
#       4) find object
#       5) output location based on the scale

#   Need to add in handling of multiple objects
class CircleFind(object):
    
    targetColor = (0, 0, 255)
    missedColor = (255,255,0)
    
    # constants that need to be tuned
    kHoleClosingIterations = 5
    def __init__(self):
        self.morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3), anchor=(1,1))
        self.size = None
    
    def processImage(self, img):
        heading = 0
        
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            self.bin = np.empty((h, w, 1), dtype=np.uint8)
            self.hsv = np.empty((h, w, 3), dtype=np.uint8)
            self.hue = np.empty((h, w, 1), dtype=np.uint8)
            self.sat = np.empty((h, w, 1), dtype=np.uint8)
            self.val = np.empty((h, w, 1), dtype=np.uint8)
           
        # convert to HSV color space
        cv2.cvtColor(img, cv2.cv.CV_BGR2HSV, self.hsv)
        cv2.split(self.hsv, [self.hue, self.sat, self.val])
        
        # Thresh out the hue
        cv2.threshold(self.hue, 80, 255, type=cv2.THRESH_BINARY_INV, dst=self.bin)
        cv2.threshold(self.hue, 40, 255, type=cv2.THRESH_BINARY, dst=self.hue)
        cv2.bitwise_and(self.bin, self.hue, self.hue)
    
        # Thresh out the saturation 
        cv2.threshold(self.sat, 55, 255, type=cv2.THRESH_BINARY, dst=self.sat)


        # Thresh out the value
        cv2.threshold(self.val, 220, 255, type=cv2.THRESH_BINARY_INV, dst=self.bin)
        cv2.threshold(self.val, 160, 255, type=cv2.THRESH_BINARY, dst=self.val)
        cv2.bitwise_and(self.val, self.bin, self.val)

    
        cv2.bitwise_and(self.hue, self.sat, self.bin)
        cv2.bitwise_and(self.bin, self.val, self.bin)
        
        # Run the morphology filter
        cv2.morphologyEx(self.bin, cv2.MORPH_CLOSE, self.morphKernel, dst=self.bin, iterations=self.kHoleClosingIterations)
        
        # Find the contours 
        contours = self.findConvexContours(self.bin)
        target = []
        squares = []
        max_rad = 0.0
        for c in contours:
            if self.isCircle(c):                
                center, radius = cv2.minEnclosingCircle(c) 
                if radius > max_rad:
                    target = (center, radius)
                    max_rad = radius
            else:
                x, y, w, h = cv2.boundingRect(c)
                ratio = float(h)/w
                if ratio < 1.0 and ratio > 0.5:
                    poly = cv2.approxPolyDP(c, 20, False)
                    squares.append((poly, x, y, w, h))
                        
        # Do some quick error checking
        if target == 0:
            print "O nose!!! No appropriate targets found..."
            return img
        if len(squares) == 0:
            print "O nose!!! No polygons were found..."
        for s in squares:
            if len(s[0]) != 4:
                print "O nose!!! Not enough points found..."
                
            # Find the center
            slope = ( float(s[2] - s[4]) / (s[1] - s[3]) )
            print slope
            cX = s[1] + int(s[3]/2.0)
            cY = s[2] + int(s[4]/2.0)
            # Find the direction
            (sX, sY)  = self.getPoint(50, slope, (cX, cY), True)
            print "other is: " + str((sX, sY))
            print "center is: " + str((cX, cY))
            cv2.circle(img, (cX, cY), 5, self.targetColor)
            cv2.line(img, (sX, sY), (cX, cY), self.targetColor)
        (x,y) = target[0]
        cv2.circle(img, (int(x),int(y)) , 5, self.targetColor)
        return img

    # Check if the contour is circular enough
    def isCircle(self, fig):
        arc = .01 * cv2.arcLength(fig, True)
        fig = cv2.approxPolyDP(fig, arc, True)
        if len(fig) >= 6:
            return True
        return False

    # Returns a list of all the convex contours 
    def findConvexContours(self, img): 
        img = img.copy()
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.cv.CV_CHAIN_APPROX_TC89_KCOS)
        return [cv2.convexHull(c, clockwise=True, returnPoints=True) for c in contours]

    def getPoint(self, dist, slope, curr, perp=False):
        if perp is True:
            slope = -1.0 / slope
            print "flipping the slope"
        retX = curr[0] + (dist / slope)
        retY = curr[1] + (dist * slope) 
        return (int(retX), int(retY))

if __name__ == '__main__':
    
    prg = CircleFind()
    
    end_time = 0.0    
    img = cv2.imread("images/img7copy.jpg")
    start_time = time.time()
    img = prg.processImage(img)
    end_time = time.time()
    cv2.imshow('Processed', img)
    
    print "runtime is: " + str(end_time - start_time)
    print "Hit ESC to exit"
    while True:
        key = 0xff & cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            break
