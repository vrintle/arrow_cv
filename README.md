# arrow_cv

## Steps involved:

- Opening the webcam / video file, if provided through `sys.argv`, using `cv2#VideoCapture`

![initial](https://i.stack.imgur.com/8exnN.jpg)

- Then, using `cv2#inRange`, select all the pixels in the custom red color range -> `[0, 0, 120] -> [50, 50, 255]`
- Then, create a mask of the captured pixels on the image, using `cv2#bitwise_and` and selection

![masked](https://i.stack.imgur.com/ABNBI.jpg)

- To thresholding image, we first convert it to grayscale colorspace, by using `cv2#cvtColor`

![grayed](https://i.stack.imgur.com/AgUbI.jpg)

- Next, we'll threshold the image to get a binary image using `cv2#threshold`

![threshold](https://i.stack.imgur.com/nuDbS.jpg)

- After that, we could have some tiny islands/holes in our binary image, which we'll remove using `cv2#erode` and `cv2#dilate` respectively
- Then, to smooth the edges for better approximation, we will use `cv2#medianBlur`

![blurred](https://i.stack.imgur.com/10JTD.jpg)

- After that, we will find the contours in our image, using `cv2#findContours`, in which we use `SIMPLE` approx to save a lot of memory
- And, then we'll iterate through contours to approximate the polygons, using an `epsilon` value calculated by `arcLength` of contour
- Now, as we have all those polygons, we've to select only the arrow, so we'll select those having `sides = 7` and `minArea = 1000.0`
- This will possibly give us only the arrow shape, _mostly_
- Now we'll iterate on each vertex, like

```
for i in range(7):
	if i == 6: # if it's the last index, take first element
		theta = np.arctan2 (
			pts[i][1] - pts[0][1], # diff of their y-coord 
			pts[i][0] - pts[0][0] # diff of their x-coord
		)

	else: # else take consecutive elements
		theta = np.arctan2 (
			pts[i][1] - pts[i+1][1], 
			pts[i][0] - pts[i+1][0]
		)

	# limit the theta in 0..360 and append it to inclinations
	inc.append((theta * 180 / np.pi + 360) % 360)
```

- Now, we have inclinations of every lines, let's find the difference

```
for i in range(7):
	if i == 6: # the same logic as in prev loop
		diff = abs(inc[i] - inc[0]) # diff of first and last
	else:
		diff = abs(inc[i] - inc[i+1]) # diff of consectutive elem

	# append the angles rounded to nearest multiple of 45 deg
	ang.append(round(diff / 45) * 45)

deg = [a % 90 for a in ang] # take the angles in I quad
```

- Now, we've the side angles too, we've to just __find the index of 90 deg in between two 45 deg__, as

```
if deg.count(45) == 2: # if only two 45 deg are there
	f = deg.index(45) # the first 45 deg
	l = 6 - deg[::-1].index(45) # the last 45 deg

	# the following if-else extract the index of 90deg when it's in between and when it's not
	if abs(f-l) == 2: # it's in between
		direc = inc[(f+l)//2]
	elif l == 5: # 90deg is at last
		direc = inc[6]
	elif f == 1: # 90deg is at first
		direc = inc[0]

	direc = ((direc - 45) + 360) % 360 
	# remove the extra 45deg inclination which the arrow head has, and limit it in 0..360

	print(direc) # print IT!!
```

- That's the whole working I have done, thanks for reading it :)
