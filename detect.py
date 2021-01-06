import cv2
import numpy as np

lower = np.array([0, 0, 120])
upper = np.array([50, 50, 255])
cap = cv2.VideoCapture(0)

while True:
	_, frame = cap.read()
	# cv2.imshow("bgr", frame)
	mask = cv2.inRange(frame, lower, upper)
	masked = cv2.bitwise_and(frame, frame, mask = mask)
	# cv2.imshow("masked", masked)

	gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)

	cv2.erode(thresh, np.ones((1,1)), iterations = 100)
	cv2.dilate(thresh, np.ones((1,1)), iterations = 100)

	thresh = cv2.medianBlur(thresh, 3)

	ctrs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	for ctr in ctrs:
		approx = cv2.approxPolyDP(ctr, 0.03 * cv2.arcLength(ctr, True), True)
		pts = [(ary[0][0], ary[0][1]) for ary in approx]
		inc = []
		ang = []

		# print(len(approx), cv2.contourArea(ctr))
		if len(pts) == 7 and cv2.contourArea(ctr) > 1e3:
			cv2.drawContours(thresh, ctrs, -1, (0, 0, 255), 2)
			for i in range(7):
				if i == 6:
					theta = np.arctan2(pts[i][1] - pts[0][1], pts[i][0] - pts[0][0])
				else:
					theta = np.arctan2(pts[i][1] - pts[i+1][1], pts[i][0] - pts[i+1][0])
				inc.append((theta * 180 / np.pi + 360) % 360)
			# print(inc)

			for i in range(7):
				if i == 6:
					diff = abs(inc[i] - inc[0])
				else:
					diff = abs(inc[i] - inc[i+1])
				ang.append(round(diff / 45) * 45)
			# print(ang)

			deg = [a % 90 for a in ang]
			if deg.count(45) == 2:
				f = deg.index(45)
				l = 6 - deg[::-1].index(45)

				if abs(f-l) == 2:
					direc = inc[(f+l)//2]
				elif l == 5:
					direc = inc[6]
				elif f == 1:
					direc = inc[0]
				direc = ((direc - 45) + 360) % 360
				print(direc)

	cv2.imshow("thresh", thresh)
	if cv2.waitKey() == 27: # check for Esc press
		break

cap.release()
