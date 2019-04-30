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
		
		self.initUI()
		
		# self.webcam()
		# self.Face()
		
		self.shapeArray = None
		
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
			
			# For each detected face, find the landmark.
			if self.faceShapePredictorActivated == True:
				count = 0
				
				for (i, rect) in enumerate(rects):
					# Make the prediction and transfom it to numpy array
					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)
				
					# Draw on our image, all the finded cordinate points (x,y)
					
					for (x, y) in shape:
							
						if count > 47:
							cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
								
						else:
							cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)

						count = count + 1
					
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
		dark_palette.setColor(QPalette.BrightText, Qt.red)
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
	 
		# Labels
		# Open Mouth
		self.openMouthlbl = QLabel("Open Mouth", self)		
		self.openMouthlbl.move(65, 50)
		# Eyebrows
		self.eyebrowslbl = QLabel("Eyebrows", self)
		self.eyebrowslbl.move(170, 50)
		# Smile
		self.smilelbl = QLabel("Smile", self)
		self.smilelbl.move(280, 50)
		# Bottom Label
		#self.styleChoice = QLabel("Option 1: A", self)
		#self.styleChoice.move(50,180)

		# CheckBoxes
		# Open Mouth
		self.b = QCheckBox("",self)
		self.b.move(87, 64)
		self.b.resize(320,40)
		self.b.stateChanged.connect(self.clickBox)
		# Eyebrows
		self.g = QCheckBox("",self)
		self.g.move(187, 64)
		self.g.resize(320,40)
		self.g.stateChanged.connect(self.clickBox)
		# Smile
		self.g = QCheckBox("",self)
		self.g.move(287, 64)
		self.g.resize(320,40)
		self.g.stateChanged.connect(self.clickBox)
		
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

	def clickBox(self, state):
		pass
		# if state == QtCore.Qt.Checked:
			# print('Checked')
		# else:
			# print('Unchecked')
		q
	@pyqtSlot()
	def on_click_initialize(self):
		if self.faceShapePredictorActivated == True:
			self.faceShapePredictorActivated = False
			
		elif self.faceShapePredictorActivated == False:
			self.faceShapePredictorActivated = True
	
	# This method captures the points of the face, so we can detect the differences between the values.
	def on_click_capture(self):
		pass
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())