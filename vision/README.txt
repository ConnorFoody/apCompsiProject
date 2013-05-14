This is a more detailed description of the process done in each image file. The “Blob” program is the main because it is both faster and more robust- 100% of test images found in an average run time of .015 seconds. The Canny/Hough detector tested a more sophisticated approach in which edges then circles are computed out of a raw image. While this method is potentially more robust, its increased processing power and tuning time leave it no significant advantages over the blob detector. 
Blob detection overview:

1)	Process the image - Converts to HSV, threshold then “fix” the image
2)	Find convex contours - Computes the closed contours for the image
3)	Find circular contours - Basic feature detection sorts circular objects


Processing:
First, we converted the image to the HSV (Hue, Saturation, Value) color space as we like it more than OpenCV’s BGR color space. In general the overlap found within the RGB color space is relatively inflexible with variable lighting or reflection. However, the HSV color space offers a much more intuitive approach to thresh holding because it focuses on more natural values like hue or saturation. Therefore, as a result of greater flexibility and ease of use, we chose the HSV color space for this project. 
For thresh holding, the saturation and value channels use a two sided thresh- a binary then inverse binary- while the hue channel uses a single binary threshold. We selected this thresh holding scheme after finding simple binary threshold insufficient on all but the hue channel.  Finally the channels are merged together into a single binary image with simple bitwise functions.  
To round out the processing, we run a morphological kernel over the binary image to repair any gaps caused by the thresholds. This step is crucial to blob detection as the contouring requires (mostly) convex outlines. This algorithm recursively dilates then erodes the image with a 3 by 3 rectangular mask 9 times. We selected the closing operation as it satisfies all our needs- implementation of the other morphological operators would again be overkill.  

Contouring: 
We look for convex (closed, non-overlapping) contours in the image. Generally this step is pretty quick, simple and robust- basically it just looks for continuous paths around the exterior of an object.  While less exact then fitting a circle or ellipse to the threshed values, contouring finds all the irregular blobs a simple fitted shape cannot. This algorithm is implemented in a helper function named “findConvexContours” to help keep the code a little cleaner. 
We start with pulling contours from the image with a simple “poly-chains” algorithm. Then, the function preforms a check to see if each contour is convex or not using the convex hull algorithm. By excluding non-convex hulls, we generate a list of all the convex contours in the image. 

Contour evaluation: 
This step checks each convex contour- found in the previous step- to see if it looks round enough. The thought is that a trapezoidal or square blob is probably not the elliptical target, so we should specify that we are looking for circular blobs. 
First we calculate an arc shape descriptor of the shape’s contour. Next, we feed the arc into a simple polygon approximation algorithm to determine the shape’s complexity. If the complexity is relatively high, we assume the figure is probably round enough and add it to the target list. Each contour in the target list is roundish, so we can go ahead and fit a circle to it. While a circle isn’t the most appropriate shape, it provides a quick and easy measurement of both center and radius. We thought about calculating image moments, but don’t see an advantage unless this method is too inaccurate. Wrap this stage up by drawing circles over the found target centers. 
