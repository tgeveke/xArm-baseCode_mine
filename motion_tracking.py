class Motion_tracking:
	print('In Motion_tracking class')
	import cv2, sys, pyrealsense2 as py2, time
	from realsense_depth import DepthCamera

	def getDistance(self):
		print('getDistance() function')
		try:
			# Read video
			video = self.cv2.VideoCapture(1)
			video.set(15, -5)
			cameraObject = self.DepthCamera() # Runs init() function
			ret, depth_frame, color_frame = cameraObject.get_frame()
		except:
			# Exit if video not opened
			print('Could not open video')
			self.sys.exit()

		self.time.sleep(1)

		# Read first frame.
		assert video.isOpened()

		ok, frame = video.read()
		if not ok:
			print('Cannot read video frame')
			ok, frame = video.read()
			#self.sys.exit()

		# Define an initial bounding box
		bbox = (287, 23, 86, 320)

		# Uncomment the line below to select a different bounding box
		# bbox = self.cv2.selectROI(frame, False)

		try:
			# Set up tracker.
			tracker = self.cv2.TrackerMIL_create()

			if frame:
				# Initialize tracker with first frame and bounding box
				ok = tracker.init(frame, bbox)
		except:
			print('Error initializing tracker')
			self.sys.exit()

		while ok:
			# Read a new frame
			ok, frame = video.read()
		if not ok:
			print('Failure')			
			self.sys.exit()

		# Start timer
		timer = cv2.getTickCount()

		# Update tracker
		ok, bbox = tracker.update(frame)

		# Calculate Frames per second (FPS)
		fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

		# Draw bounding box
		if ok:
			# Tracking success
			p1 = (int(bbox[0]), int(bbox[1]))

			p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

			pp2 = (int(bbox[0] + (bbox[2] / 2)), int(bbox[1] + (bbox[3]) / 2))

			# find the center of the frame to due the depth calculation

			cv2.circle(frame, pp2, 4, (0, 0, 255))
			distance = depth_frame[pp2]
			cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
			
			return distance
		else:
			# Tracking failure
			cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

		# Display tracker type on frame
		cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

		# Display FPS on frame
		cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

		# Display result
		cv2.imshow("Tracking", frame)

		# Exit if ESC pressed
		k = cv2.waitKey(1) & 0xff


if __name__ == '__main__':
	obj = Motion_tracking()
	obj.getDistance()
