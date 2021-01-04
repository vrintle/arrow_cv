import cv2
import numpy as np

lower = np.array([0, 0, 80])
upper = np.array([30, 30, 255])
cap = cv2.VideoCapture(0)

while True:
	# frame = cv2.imread("redarrow.jpg")
	_, frame = cap.read()
	frame = cv2.medianBlur(frame, 3)
	# cv2.imshow("bgr", frame)
	mask = cv2.inRange(frame, lower, upper)
	masked = cv2.bitwise_and(frame, frame, mask = mask)
	# cv2.imshow("masked", masked)

	gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
	# cv2.imshow("dilated", dilate)
	_, thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)
	# kernel = np.ones((2,2), np.uint8) 
	# thresh = cv2.erode(thresh, kernel, iterations = 3)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
	cv2.imshow("thresh", thresh)

	cntrs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	for cntr in cntrs:
		approx = cv2.approxPolyDP(cntr, 0.03 * cv2.arcLength(cntr, True), True)
		print("sides:", len(approx))

	# cv2.imshow("final", thresh)
	# cv2.waitKey(0)
	if cv2.waitKey() == 27: # check for Esc press
		break

cap.release()
