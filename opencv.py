from imutils.video import VideoStream
from imutils.video import FPS
from skimage.measure import compare_ssim
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import time
import cv2
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())
image=cv2.imread("back_ground.jpg")
graybg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cap = cv2.VideoCapture(0)
i=0
temp=0
fps = int(cap.get(5))
print("fps:", fps)
while True:
    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(gray, graybg, full=True)
    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    edged = cv2.Canny(thresh, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
       cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    for c in cnts:
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) < 10000:
		continue
        orig = img.copy()
	box = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
	box = perspective.order_points(box)
	(tl, tr, br, bl) = box
	(tltrX, tltrY) = midpoint(tl, tr)
	(blbrX, blbrY) = midpoint(bl, br)
	(tlblX, tlblY) = midpoint(tl, bl)
	(trbrX, trbrY) = midpoint(tr, br)
	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
	if pixelsPerMetric is None:
		pixelsPerMetric = dB / 10
	dimA = dA / pixelsPerMetric
	dimB = dB / pixelsPerMetric
	cv2.putText(orig, "{:.1f}in".format(dimA),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
	cv2.putText(orig, "{:.1f}in".format(dimB),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
    # Display
        
        velocity= (dimA-temp)/.033
        print(velocity)
        temp= dimA
    cv2.imshow("img", thresh)

    # Stop if escape key is pressed
    key=cv2.waitKey(1)
    if key%256 == 27:
        break
        
# Release the VideoCapture object
cap.release()
