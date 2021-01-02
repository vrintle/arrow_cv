import cv2, numpy

cap = cv2.VideoCapture(0)
while True:
	_, frame = cap.read()
	img = cv2.medianBlur(frame, 5)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	_, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
	cntrs, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	for cntr in cntrs:
		approx = cv2.approxPolyDP(cntr, 0.01 * cv2.arcLength(cntr, True), True)
		if len(approx) != 4:
			cv2.drawContours(img, [approx], 0, (0, 0, 255),
			 2)
			print("That's my arrow")

	cv2.imshow("arrow", img)
	if cv2.waitKey() == 27: # check for Esc press
		break

cap.release()
