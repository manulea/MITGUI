import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSlot, QSize, Qt
import cv2

from imutils import face_utils
import numpy as np

import dlib

class App(QWidget):
	def __init__(self):
		super().__init__()
		
		self.title = 'Face Recognition'
		
		self.left = 200
		self.top = 200
		self.width = 400
		self.height = 200
		
		self.setWindowIcon(QtGui.QIcon('icon.png'))
		self.captureFacePositions = False
		self.capturedPositions = False
		self.initUI()
		
		# Smile
		self.LeftSideMouth = 0
		self.RightSideMouthSide = 0
					
		self.capturedLeftSideMouth = 0
		self.capturedRightSideMouth = 0
		
		# Eyebrows
		self.EyebrowLeft = 0
		self.EyebrowRight = 0
		self.EyeTopLeft = 0
		self.EyeTopRight = 0
		
		self.capturedEyebrowLeft = 0
		self.capturedEyebrowRight = 0
		
		self.smileActivated = False
		self.openMouthActivated = False
		self.raiseEyebrowsActivated = False
		
		self.faceShapePredictorActivated = False
		self.landmarks()

		
	def webcam(self):
		cap = cv2.VideoCapture(0)

		while(True):
			# Capture frame-by-frame
			ret, frame = cap.read()

			# Our operations on the frame come here
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# Display the resulting frame
			cv2.imshow('hey', gray)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
	
	def Face(self):
		cascPath = sys.argv[1]
		faceCascade = cv2.CascadeClassifier(cascPath)
		#smile_cascade = cv2.CascadeClassifier(casc
		video_capture = cv2.VideoCapture(0)
		while True:
			# Capture frame-by-frame
			ret, frame = video_capture.read()

			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			faces = faceCascade.detectMultiScale(
				gray,
				scaleFactor = 1.1,
				minNeighbors = 5,
				minSize = (30, 30),
				# flags = cv2.cv.CV_HAAR_SCALE_IMAGE
				flags = cv2.CASCADE_SCALE_IMAGE
			)

			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

			# Display the resulting frame
			cv2.imshow('Video', frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# When everything is done, release the capture
		video_capture.release()
		cv2.destroyAllWindows()

	def landmarks(self):
		# Vamos inicializar um detector de faces (HOG) para então
		# let's go code an faces detector(HOG) and after detect the 
		# landmarks on this detected face

		# p = our pre-treined model directory, on my case, it's on the same script's diretory.
		p = "shape_predictor_68_face_landmarks.dat"
		
		detector = dlib.get_frontal_face_detector()
		predictor = dlib.shape_predictor(p)

		cap = cv2.VideoCapture(0)
		 
		while True:
			# Getting out image by webcam 
			_, frame = cap.read()
			# Converting the image to gray scale
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				
			# Get faces into webcam's image
			rects = detector(gray, 0)
			
			count = 0
			
			# For each detected face, find the landmark.
			if self.faceShapePredictorActivated == True:
				
				for (i, rect) in enumerate(rects):
					# Make the prediction and transfom it to numpy array
					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)

					# Draw on our image, all the finded cordinate points (x,y)
					
					#cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
					#cv2.line(frame, (x, y+50), (x, y-50), (255, 102, 255), thickness=1, lineType=8, shift=0)
					#cv2.line(frame, (x, y+50), (x, y-50), (255, 102, 255), thickness=1, lineType=8, shift=0)
					
					for (x, y) in shape:
					
						# SMILE
						if (count == 48):
							if self.smileActivated == True:
								if (self.captureFacePositions == True):
									self.capturedLeftSideMouth = x
									
							self.LeftSideMouth = (x)
							
						if (count == 54):
							if self.smileActivated == True:
								if (self.captureFacePositions == True):
									self.capturedRightSideMouth = x
									
							self.RightSideMouthSide = (x)
						
						if (self.captureFacePositions == True):
							if (self.capturedRightSideMouth >= 0 and self.capturedLeftSideMouth >= 0):
								self.capturedPositions = True
						# END SMILE
						
						# RAISE EYEBROW
						if (count == 19):
							if self.raiseEyebrowsActivated == True:
								
								if (self.captureFacePositions == True):
									self.EyebrowLeft = y
									
								self.capturedEyebrowLeft = y
								
						if (count == 24):
							if self.raiseEyebrowsActivated == True:
								if (self.captureFacePositions == True):
									self.EyebrowRight = y
								
							self.capturedEyebrowRight = y
							
						if (self.captureFacePositions == True):
							if (self.capturedEyebrowLeft >= 0 and self.capturedEyebrowRight >= 0):
								self.capturedPositions = True
						
						# END RAISE EYEBROW
						
						if count >= 48:
							cv2.circle(frame, (x, y), 2, (255, 200, 255), -1)
						
						if count == 1:

							w = 200
							h = 180
							cv2.rectangle(frame, (x-30, y-100), (x+w, y+h), (0, 255, 0), 2)
			
						elif (count < 48):
							cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
						
						font = cv2.FONT_HERSHEY_SIMPLEX
						
						# Could be used for face identity
						# Detect smiles
						if count == 34:
							cv2.putText(frame, ("sione"), (x-40, y+180), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
						
						count = count + 1

					if self.captureFacePositions == True:
						print("Successfully captured positions")					
						self.captureFacePositions = False
					
					if (self.capturedPositions == True):
						#print(LeftSideMouth)
						#print(capturedLeftSideMouth)
						if self.smileActivated == True:
							if (self.RightSideMouthSide - self.LeftSideMouth - 8 > self.capturedRightSideMouth - self.capturedLeftSideMouth):
								print("Smiled")
						elif self.openMouthActivated == True:
							pass
							
							
						elif self.raiseEyebrowsActivated == True:
							#if (self.EyebrowLeft - 1 < self.capturedEyebrowLeft and self.EyebrowRight - 1 < self.capturedEyebrowRight):
							#if (self.EyebrowLeft < 
							#	print(
							pass
						
					
			# Show the image
			cv2.imshow("Output", frame)
				
			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break
			# Press 'q' to break out of loop
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
				
		cv2.destroyAllWindows()
		cap.release()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		QApplication.setStyle(QtWidgets.QStyleFactory.create('dark-Fusion'))
		
		# Introducing - The QPalette 
		dark_palette = QPalette()

		dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.WindowText, Qt.green)
		dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
		dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		dark_palette.setColor(QPalette.Text, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ButtonText, Qt.white)
		#dark_palette.setColor(QPalette.BRightSideMouthText, Qt.red)
		dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.HighlightedText, Qt.black)
		QApplication.setPalette(dark_palette)

		#QApplication.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
		
		self.setStyleSheet("QPushButton { background-color: gray; }\n"
              "QPushButton:enabled { background-color: green; }\n");
			  
		# Buttons 
		btnInitialize = QPushButton('Initialize', self)
		btnInitialize.setToolTip('Activate face detection')
		btnInitialize.move(100,140)
		btnInitialize.clicked.connect(self.on_click_initialize)

		btnCapture = QPushButton('Capture Face', self)
		btnCapture.setToolTip('Used to capture the initial face array.')
		btnCapture.move(200,140)
		btnCapture.clicked.connect(self.on_click_capture)
	 
		# # Labels
		
		# # Open Mouth
		# self.openMouthlbl = QLabel("Open Mouth", self)		
		# self.openMouthlbl.move(65, 50)
		# # Eyebrows
		# self.eyebrowslbl = QLabel("Eyebrows", self)
		# self.eyebrowslbl.move(170, 50)
		# # Smile
		# self.smilelbl = QLabel("Smile", self)
		# self.smilelbl.move(280, 50)
		# # Bottom Label
		# #self.styleChoice = QLabel("Option 1: A", self)
		# #self.styleChoice.move(50,180)

		# CheckBoxes
		# Open Mouth
		self.checkboxOpenMouth = QCheckBox("Open Mouth",self)
		self.checkboxOpenMouth.move(87, 64)
		self.checkboxOpenMouth.resize(320,40)
		self.checkboxOpenMouth.stateChanged.connect(lambda:self.btnState(self.checkboxOpenMouth))
		# Raise Eyebrows
		self.checkboxRaiseEyebrows = QCheckBox("Raise Eyebrows",self)
		self.checkboxRaiseEyebrows.move(187, 64)
		self.checkboxRaiseEyebrows.resize(320,40)
		self.checkboxRaiseEyebrows.stateChanged.connect(lambda:self.btnState(self.checkboxRaiseEyebrows))
		# Smile
		self.checkboxSmile = QCheckBox("Smile",self)
		self.checkboxSmile.move(287, 64)
		self.checkboxSmile.resize(320,40)
		self.checkboxSmile.stateChanged.connect(lambda:self.btnState(self.checkboxSmile))
		
		# ComboBox
		# Open Mouth
		comboBox = QtWidgets.QComboBox(self)
		comboBox.addItem("Option 1")
		comboBox.addItem("Option 2")
		comboBox.move(50, 100)
		
		comboBox.activated[str].connect(self.style_choice)
		
		# Eyebrows
		comboBox2 = QtWidgets.QComboBox(self)
		comboBox2.addItem("Option 1")
		comboBox2.addItem("Option 2")
		comboBox2.move(150, 100)
		
		comboBox2.activated[str].connect(self.style_choice)
		
		# Smile
		comboBox3 = QtWidgets.QComboBox(self)
		comboBox3.addItem("Option 1")
		comboBox3.addItem("Option 2")
		comboBox3.move(250, 100)

		comboBox3.activated[str].connect(self.style_choice)

		self.show()
		
	def style_choice(self, text):
		self.styleChoice.setText(text)

	def btnState(self, state):
		if state.text() == "Smile":
			if state.isChecked() == True:
				if (self.smileActivated == False):
					print("Smile Detection Activated")
					self.smileActivated = True
			else:
				self.smileActivated = False
				print("Smile Detection Deactivated")
				
		if state.text() == "Raise Eyebrows":
			if state.isChecked() == True:
				if (self.raiseEyebrowsActivated == False):
					print("Raise Eyebrows Detection Activated")
					self.raiseEyebrowsActivated = True
			else:
				self.raiseEyebrowsActivated = False
				print("Raise Eyebrows Detection Deactivated")
								
		if state.text() == "Open Mouth":
			if state.isChecked() == True:
				if (self.openMouthActivated == False):
					print("Open Mouth Detection Activated")
					self.openMouthActivated = True
			else:
				self.openMouthActivated = False
				print("Open Mouth Detection Deactivated")								
								
		# if state == QtCore.Qt.Checked:
			# print('Checked')
		# else:
			# print('Unchecked')
			
	@pyqtSlot()
	def on_click_initialize(self):
		if self.faceShapePredictorActivated == True:
			self.faceShapePredictorActivated = False
			
		elif self.faceShapePredictorActivated == False:
			self.faceShapePredictorActivated = True
	
	# This method captures the points of the face, so we can detect the differences between the values.
	def on_click_capture(self):
		if (self.faceShapePredictorActivated == True):
			self.captureFacePositions = True
			print("Capturing positions")
			
		elif (self.faceShapePredictorActivated == False):
			print("Required: Initialization")
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())