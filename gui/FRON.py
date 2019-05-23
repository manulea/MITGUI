import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSlot, QSize, Qt

from imutils import face_utils
import numpy as np

import cv2
import dlib

from pyautogui import press, typewrite, hotkey

class App(QWidget):
	def __init__(self):
		super().__init__()
		
		self.title = 'Face Recognition'
		
		self.left = 200
		self.top = 200
		self.width = 400
		self.height = 200
		
		self.setWindowIcon(QtGui.QIcon('icon.png'))
		self.captureFacePositions = True
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
		
		self.capturedEyeTopLeft = 0
		self.capturedEyeTopRight = 0
		self.capturedEyebrowLeft = 0
		self.capturedEyebrowRight = 0
		
		# Open Mouth
		self.topMouth = 0
		self.bottomMouth = 0
		
		self.capturedTopMouth = 0
		self.capturedBottomMouth = 0
		
		# Snarl
		self.snarlLeftEyebrowTip = 0
		self.snarlRightEyebrowTip = 0
		
		self.snarlTopNose = 0
		self.snarlEyeTopCenterLeft = 0
		self.snarlEyeBotCenterLeft = 0
		
		self.snarlEyeTopCenterRight = 0
		self.snarlEyeBotCenterRight = 0
		
		self.snarlCenterChin = 0
		self.snarlCenterNose = 0
		
		# Snarl
		self.CapturedsnarlLeftEyebrowTip = 0
		self.CapturedsnarlRightEyebrowTip = 0
		
		self.CapturedsnarlTopNose = 0
		self.CapturedsnarlEyeTopCenterLeft = 0
		self.CapturedsnarlEyeBotCenterLeft = 0
		
		self.CapturedsnarlEyeTopCenterRight = 0
		self.CapturedsnarlEyeBotCenterRight = 0
		
		self.CapturedsnarlCenterChin = 0
		self.CapturedsnarlCenterNose = 0
		
		self.smileActivated = False
		self.openMouthActivated = False
		self.raiseEyebrowsActivated = False
		self.snarlActivated = False
		
		self.faceShapePredictorActivated = False
		
		self.landmarks()

	def landmarks(self):
		# p = our pre-treined model directory, on my case, it's on the same script's diretory.
		p = "shape_predictor_68_face_landmarks.dat"
		
		detector = dlib.get_frontal_face_detector()
		predictor = dlib.shape_predictor(p)

		cap = cv2.VideoCapture(0)
		 
		T = [[ 239, 181],
				[239, 208],
				[241, 234],
				[245, 259],
				[253, 283],
				[268, 302],
				[287, 317],
				[307, 330],
				[329, 333],
				[351, 329],
				[370, 316],
				[390, 303],
				[406, 285],
				[417, 263],
				[422, 239],
				[424, 214],
				[425, 188],
				[256, 169],
				[267, 157],
				[284, 152],
				[303, 154],
				[319, 161],
				[345, 162],
				[361, 158],
				[379, 157],
				[395, 162],
				[405, 174],
				[331, 185],
				[331, 201],
				[330, 216],
				[330, 232],
				[311, 241],
				[319, 245],
				[329, 247],
				[339, 245],
				[348, 242],
				[276, 186],
				[285, 182],
				[297, 183],
				[308, 189],
				[296, 192],
				[284, 192],
				[353, 191],
				[363, 185],
				[374, 186],
				[385, 191],
				[375, 195],
				[363, 195],
				[296, 271],
				[308, 265],
				[321, 262],
				[329, 264],
				[337, 263],
				[348, 267],
				[359, 273],
				[348, 284],
				[337, 288],
				[328, 289],
				[319, 287],
				[307, 283],
				[301, 271],
				[320, 270],
				[329, 271],
				[337, 270],
				[353, 274],
				[337, 276],
				[328, 277],
				[320, 276]]
		 
		while True:
			# Getting out image by webcam 
			_, frame = cap.read()
			# Converting the image to gray scale
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				
			# Get faces into webcam's image
			rects = detector(gray, 0)
			
			if (self.faceShapePredictorActivated == False):
				for (x, y) in T:
					cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
					#cv2.circle(frame, (x, y), 2, (137, 205, 230), -1)
					
			# For each detected face, find the landmark.
			if (self.faceShapePredictorActivated == True):
				
				for (i, rect) in enumerate(rects):
					# Make the prediction and transfom it to numpy array
					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)
					
					count = 1

					# Draw on our image, all the found coordinate points (x,y)
					for (x, y) in shape:
						# draw all the points in shape (x,y)
						if count >= 0 and count <= 68:
							#cv2.circle(frame, (x, y), 2, (255, 200, 255), -1)
							cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
						# display text underneath the face object
						if count == 9:
							font = cv2.FONT_HERSHEY_SIMPLEX
							cv2.putText(frame, ("text"), (x - 40, y + 70), font, 1, (255, 255, 255), 1, cv2.LINE_AA)	
						# raise eyebrow
						# left eyebrow
						elif (count == 20):
							if (self.captureFacePositions == True):
								self.capturedEyebrowLeft = y	
								
							if self.raiseEyebrowsActivated == True:
								self.EyebrowLeft = y
						# snarl
						elif (count == 22):
							if (self.captureFacePositions == True):
								self.CapturedsnarlLeftEyebrowTip = y
							if (self.snarlActivated == True):
								self.snarlLeftEyebrowTip = y
						elif (count == 23):
							if (self.captureFacePositions == True):
								self.CapturedsnarlRightEyebrowTip = y
							if (self.snarlActivated == True):
								self.snarlRightEyebrowTip = y
						elif (count == 28):
							if (self.captureFacePositions == True):
								self.CapturedsnarlCenterNose = y
							if (self.snarlActivated == True):
								self.snarlCenterNose = y
						elif (count == 42):
							if (self.captureFacePositions == True):
								self.CapturedsnarlEyeBotCenterLeft = y
							if (self.snarlActivated == True):
								self.snarlEyeBotCenterLeft = y
						elif (count == 48):
							if (self.captureFacePositions == True):
								self.CapturedsnarlEyeBotCenterRight = y
							if (self.snarlActivated == True):
								self.snarlEyeBotCenterRight = y							
						
						# right eyebrow
						elif (count == 25):
							if self.raiseEyebrowsActivated == True:
								self.EyebrowRight = y
								
							if (self.captureFacePositions == True):
								self.capturedEyebrowRight = y
									
						# left eye
						elif (count == 38): 
							if self.raiseEyebrowsActivated == True  or self.snarlActivated == True:
								self.EyeTopLeft = y
								
							if (self.captureFacePositions == True):
								self.capturedEyeTopLeft = y
								
						# right eye
						elif (count == 44):
							if self.raiseEyebrowsActivated == True  or self.snarlActivated == True:
								self.EyeTopRight = y
								
							if (self.captureFacePositions == True):
								self.capturedEyeTopRight = y
						# end eyebrow
						# smile
						elif (count == 49):
							if (self.captureFacePositions == True):
								self.capturedLeftSideMouth = x	
								
							if self.smileActivated == True:
								self.LeftSideMouth = (x)
							
						elif (count == 55):
							if (self.captureFacePositions == True):
								self.capturedRightSideMouth = x
								
							if self.smileActivated == True:
								self.RightSideMouthSide = (x)
						# end smile
						# open mouth
						elif (count == 52):
							if (self.openMouthActivated == True):
								self.topMouth = y
								
							if (self.captureFacePositions == True):
								self.capturedTopMouth = y
								
								
						elif (count == 58):
							if (self.openMouthActivated == True):
								self.bottomMouth = y
								
							if (self.captureFacePositions == True):
								self.capturedBottomMouth = y
						# end open mouth

						count += 1

					cv2.rectangle(frame, (shape[1, 0], shape[1, 1]), (shape[9, 0], shape[9, 1]), (0, 255, 0), 8)
			
					# check if all needed positions have been captured.
					if (self.captureFacePositions == True):
						if (self.capturedTopMouth > 0 and self.capturedBottomMouth > 0):
							if (self.capturedEyebrowLeft > 0 and self.capturedEyebrowRight > 0):
								if (self.capturedRightSideMouth > 0 and self.capturedLeftSideMouth > 0):
									self.capturedPositions = True
									self.captureFacePositions = False
									print("successfully captured landmarks.")	
					
					#  when all landmarks have been captured:
					if (self.capturedPositions == True):
						# smile
						if self.smileActivated == True:
							if (self.RightSideMouthSide - self.LeftSideMouth - 8 > self.capturedRightSideMouth - self.capturedLeftSideMouth):
								print("smile detected")
						# mouth
						if self.openMouthActivated == True:
							if (self.bottomMouth - self.topMouth - 5 > self.capturedBottomMouth - self.capturedTopMouth):
								print("open mouth detected")
						# eyebrow raised
						if self.raiseEyebrowsActivated == True:
							if ((self.capturedEyeTopLeft - self.capturedEyebrowLeft + 3 < self.EyeTopLeft - self.EyebrowLeft) and
							(self.capturedEyeTopRight - self.capturedEyebrowRight + 3 < self.EyeTopRight - self.EyebrowRight)):
								print("eyebrow detected")
								#press('a')
						# snarl
						if (self.snarlActivated == True):
							if (self.CapturedsnarlCenterNose - self.CapturedsnarlLeftEyebrowTip - 2 >= self.snarlCenterNose - self.snarlLeftEyebrowTip):
								if (self.CapturedsnarlCenterNose - self.CapturedsnarlRightEyebrowTip - 2 >= self.snarlCenterNose - self.snarlRightEyebrowTip):
									if (self.CapturedsnarlEyeBotCenterLeft - self.capturedEyeTopLeft  + 1 > self.snarlEyeBotCenterLeft - self.EyeTopLeft):
										if (self.CapturedsnarlEyeBotCenterRight - self.capturedEyeTopRight + 1 > self.snarlEyeBotCenterRight - self.EyeTopRight):
											if (self.CapturedsnarlCenterChin - self.CapturedsnarlCenterNose + 1 > self.snarlCenterChin - self.snarlCenterNose ):
												print("snarl detected")
												
												
						
			# Show the image
			cv2.imshow("Face Recognition", frame)
			
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

		self.setStyleSheet("QPushButton { background-color: gray; }\n"
              "QPushButton:enabled { background-color: green; }\n");
			  
		# Buttons 
		btnInitialize = QPushButton('activate', self)
		btnInitialize.setToolTip('activate face detection')
		btnInitialize.move(100, 140)
		btnInitialize.clicked.connect(self.on_click_initialize)

		btnCapture = QPushButton('recapture', self)
		btnCapture.setToolTip('used to capture the initial face array.')
		btnCapture.move(200, 140)
		btnCapture.clicked.connect(self.on_click_capture)

		# CheckBoxes
		# Open Mouth
		self.checkboxOpenMouth = QCheckBox("open mouth",self)
		self.checkboxOpenMouth.move(30, 64)
		self.checkboxOpenMouth.resize(320, 40)
		self.checkboxOpenMouth.stateChanged.connect(lambda:self.btnState(self.checkboxOpenMouth))
		# Raise Eyebrows
		self.checkboxRaiseEyebrows = QCheckBox("raise eyebrows",self)
		self.checkboxRaiseEyebrows.move(120, 64)
		self.checkboxRaiseEyebrows.resize(320, 40)
		self.checkboxRaiseEyebrows.stateChanged.connect(lambda:self.btnState(self.checkboxRaiseEyebrows))
		# Smile
		self.checkboxSmile = QCheckBox("smile",self)
		self.checkboxSmile.move(230, 64)
		self.checkboxSmile.resize(320, 40)
		self.checkboxSmile.stateChanged.connect(lambda:self.btnState(self.checkboxSmile))
		# 
		self.checkboxSnarl = QCheckBox("snarl",self)
		self.checkboxSnarl.move(310, 64)
		self.checkboxSnarl.resize(320, 40)
		self.checkboxSnarl.stateChanged.connect(lambda:self.btnState(self.checkboxSnarl))		
		
		# ComboBox
		# Open Mouth
		comboBox = QtWidgets.QComboBox(self)
		comboBox.addItem("a")
		comboBox.addItem("b")
		comboBox.move(30, 100)
		
		comboBox.activated[str].connect(self.style_choice)
		
		# Eyebrows
		comboBox2 = QtWidgets.QComboBox(self)
		comboBox2.addItem("a")
		comboBox2.addItem("b")
		comboBox2.move(120, 100)
		
		comboBox2.activated[str].connect(self.style_choice)
		
		# Smile
		comboBox3 = QtWidgets.QComboBox(self)
		comboBox3.addItem("a")
		comboBox3.addItem("b")
		comboBox3.move(230, 100)

		comboBox3.activated[str].connect(self.style_choice)

		# Smile
		comboBox3 = QtWidgets.QComboBox(self)
		comboBox3.addItem("a")
		comboBox3.addItem("b")
		comboBox3.move(310, 100)

		comboBox3.activated[str].connect(self.style_choice)
		
		self.show()
		
	def style_choice(self, text):
		if (text == "a"):
			press('a')

	def btnState(self, state):
		# checkBox activations
		# smile checkbox
		if state.text() == "smile":
			if state.isChecked() == True:
				if (self.smileActivated == False):
					print("smile detection activated")
					self.smileActivated = True
			else:
				self.smileActivated = False
				print("smile detection deactivated")
		# raise eyebrow checkbox
		if state.text() == "raise eyebrows":
			if state.isChecked() == True:
				if (self.raiseEyebrowsActivated == False):
					print("raise eyebrows detection activated")
					self.raiseEyebrowsActivated = True
			else:
				self.raiseEyebrowsActivated = False
				print("raise eyebrows detection deactivated")
	    # open mouth checkbox
		if state.text() == "open mouth":
			if state.isChecked() == True:
				if (self.openMouthActivated == False):
					print("open mouth detection activated")
					self.openMouthActivated = True
			else:
				self.openMouthActivated = False
				print("open mouth detection deactivated")								
		# snarl checkbox
		if state.text() == "snarl":
			if state.isChecked() == True:
				if (self.snarlActivated == False):
					print("snarl detection activated")
					self.snarlActivated = True
			else:
				self.snarlActivated = False
				print("snarl detection deactivated")
		
	@pyqtSlot()
	def on_click_initialize(self):
		if self.faceShapePredictorActivated == True:
			self.faceShapePredictorActivated = False
			
		elif self.faceShapePredictorActivated == False:
			self.faceShapePredictorActivated = True
	
	# this method captures the points of the face, so we can detect the differences between the values.
	def on_click_capture(self):
		if (self.faceShapePredictorActivated == True):
			self.captureFacePositions = True
			print("capturing landmarks")
			
		elif (self.faceShapePredictorActivated == False):
			print("activate required")
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())