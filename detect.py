import cv2
import numpy as np

lower = np.array([0, 0, 100])
upper = np.array([50, 50, 255])
cap = cv2.VideoCapture(0)

while True:
	# frame = cv2.imread("redarrow.jpg")
	_, frame = cap.read()
	# frame = cv2.medianBlur(frame, 3)
	# cv2.imshow("bgr", frame)
	mask = cv2.inRange(frame, lower, upper)
	masked = cv2.bitwise_and(frame, frame, mask = mask)
	# cv2.imshow("masked", masked)

	gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
	# cv2.imshow("dilated", dilate)
	_, thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)

	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
	# thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 500)
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
	# thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 500)

	cv2.erode(thresh, np.ones((1,1)), iterations = 100)
	cv2.dilate(thresh, np.ones((1,1)), iterations = 100)

	thresh = cv2.medianBlur(thresh, 3)
	cv2.imshow("thresh", thresh)

	cntrs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	for cntr in cntrs:
		approx = cv2.approxPolyDP(cntr, 0.03 * cv2.arcLength(cntr, True), True)
		pts = [(ary[0][0], ary[0][1]) for ary in approx]
		inc = []
		ang = []
		# print(len(approx), cv2.contourArea(cntr))

		if len(pts) == 7 and cv2.contourArea(cntr) > 1e3:
			for i in range(7):
				if i == 6:
					theta = np.arctan2(pts[i][1] - pts[0][1], pts[i][0] - pts[0][0])
				else:
					theta = np.arctan2(pts[i][1] - pts[i+1][1], pts[i][0] - pts[i+1][0])
				inc.append((theta * 180 / np.pi + 180) % 180)
			print(inc)

			for i in range(7):
				if i == 6:
					diff = abs(inc[i] - inc[0])
				else:
					diff = abs(inc[i] - inc[i+1])
				ang.append(45 if abs(diff - 90) > abs(diff - 45) else 90)
			if ang.count(45) == 2:
				f = ang.index(45)
				l = ang[::-1].index(45)
				# print(f, l)
				# if l - f == 2:
					# print(inc[(f+l)//2])
				# print(ang)

	# cv2.imshow("final", thresh)
	# cv2.waitKey(0)
	if cv2.waitKey() == 27: # check for Esc press
		break

cap.release()
