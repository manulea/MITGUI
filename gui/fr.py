import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, QSize, Qt

#from PyQt5 import *
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *

from imutils import face_utils
import numpy as np

import cv2
import dlib

from pynput.keyboard import Key, Controller

keyboard = Controller()

class App(QWidget):
	def __init__(self):
		super().__init__()

		self.title = 'Face Recognition'
		
		self.left = 200
		self.top = 200
		self.width = 670
		self.height = 620
		
		self.setWindowIcon(QtGui.QIcon('icon.png'))
		self.captureFacePositions = True
		self.capturedPositions = False
		self.initUI()
				
		self.topLeftX = 0
		self.topLeftY = 0
		self.botRightX = 0
		self.botRightY = 0

		# Smile
		self.LeftSideMouth = 0
		self.RightSideMouthSide = 0
					
		self.capturedLeftSideMouth = 0
		self.capturedRightSideMouth = 0
		
		self.count = 0

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
		
		self.smiling = False
		self.openedMouth = False
		self.raisingEyebrows = False
		self.snarling = False
		
		self.faceShapePredictorActivated = False
		
		self.landmarks()

	def landmarks(self):
		# p = our pre-treined model directory, on my case, it's on the same script's diretory.
		p = "shape_predictor_68_face_landmarks.dat"
		
		detector = dlib.get_frontal_face_detector()
		predictor = dlib.shape_predictor(p)

		cap = cv2.VideoCapture(0)
		
		# Used so user knows where to put their face.
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
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				
			# Get faces into webcam's image
			rects = detector(gray, 0)
			
			#if (self.faceShapePredictorActivated == False):
				#for (x, y) in T:
					#cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
					
			# For each detected face, find the landmark.
			if (self.faceShapePredictorActivated == True):
				for (i, rect) in enumerate(rects):
					# Make the prediction and transfom it to numpy array
					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)
					
			
					self.topLeftX = 0
					self.topLeftY = 0
					self.botRightX = 0
					self.botRightY = 0


					self.count = 1

					for (x, y) in shape:
						self.leftRight(x, y, self.topLeftX, self.topLeftY, self.botRightX, self.botRightY, frame, self.count)
						self.count += 1		

					addLength = 10
					cv2.rectangle(frame, (self.topLeftX-addLength, self.topLeftY-addLength), (self.botRightX+addLength, self.botRightY+addLength), (0, 255, 0), 5)
					

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

								self.smiling = True
						# mouth
						if self.openMouthActivated == True:
							if (self.bottomMouth - self.topMouth - 5 > self.capturedBottomMouth - self.capturedTopMouth):
								print("open mouth detected")
								
								self.openedMouth = True
								
						# eyebrow raised
						if self.raiseEyebrowsActivated == True:
							if ((self.capturedEyeTopLeft - self.capturedEyebrowLeft + 3 < self.EyeTopLeft - self.EyebrowLeft) and
							(self.capturedEyeTopRight - self.capturedEyebrowRight + 3 < self.EyeTopRight - self.EyebrowRight)):
								print("eyebrow detected")
								
								self.raisingEyebrows = True
								
						# snarl
						if (self.snarlActivated == True):
							if (self.CapturedsnarlCenterNose - self.CapturedsnarlLeftEyebrowTip - 2 >= self.snarlCenterNose - self.snarlLeftEyebrowTip):
								if (self.CapturedsnarlCenterNose - self.CapturedsnarlRightEyebrowTip - 2 >= self.snarlCenterNose - self.snarlRightEyebrowTip):
									if (self.CapturedsnarlEyeBotCenterLeft - self.capturedEyeTopLeft  + 1 > self.snarlEyeBotCenterLeft - self.EyeTopLeft):
										if (self.CapturedsnarlEyeBotCenterRight - self.capturedEyeTopRight + 1 > self.snarlEyeBotCenterRight - self.EyeTopRight):
											if (self.CapturedsnarlCenterChin - self.CapturedsnarlCenterNose + 1 > self.snarlCenterChin - self.snarlCenterNose ):
												print("snarl detected")
												
												self.snarling = True
										
			# self.smiling = False
			# self.openedMouth = False
			# self.raisingEyebrows = False
			# self.snarling = False
			
			# Show the image
			# cv2.imshow("Face Recognition", frame)

			rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			image = QImage(rgb_frame.tobytes(), 
			rgb_frame.shape[1],
			rgb_frame.shape[0],
			QImage.Format_RGB888)
			
			self.webcam.setPixmap(QPixmap.fromImage(image))
			self.webcam.show()
			
			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break
			# Press 'q' to break out of loop
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
				
		cv2.destroyAllWindows()
		cap.release()

	def leftRight(self, x, y, topLeftX, topLeftY, botRightX, botRightY, frame, count):
	
		# Box - top left 
		if x > self.topLeftX and self.topLeftX == 0:
			self.topLeftX = x
			
		if x < self.topLeftX and self.topLeftX > 0:
			self.topLeftX = x
			
		if y > self.topLeftY and self.topLeftY == 0:
			self.topLeftY = y
			
		if y < self.topLeftY and self.topLeftY > 0:
			self.topLeftY = y
			
		# Box - bot right
		if x >= self.botRightX:
			self.botRightX = x
			
		if y >= self.botRightY:
			self.botRightY = y
			
		if (self.count > 0):
			if (self.count >= 0) and (self.count <= 68):
				cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)

			if (self.count == 9):
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(frame, ("text"), (x - 40, y + 70), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

			# left eyebrow
			elif (self.count == 20):
				if (self.captureFacePositions == True):
					self.capturedEyebrowLeft = y	
					
				if self.raiseEyebrowsActivated == True:
					self.EyebrowLeft = y
			# snarl
			elif (self.count == 22):
				if (self.captureFacePositions == True):
					self.CapturedsnarlLeftEyebrowTip = y
				if (self.snarlActivated == True):
					self.snarlLeftEyebrowTip = y
			elif (self.count == 23):
				if (self.captureFacePositions == True):
					self.CapturedsnarlRightEyebrowTip = y
				if (self.snarlActivated == True):
					self.snarlRightEyebrowTip = y
			elif (self.count == 28):
				if (self.captureFacePositions == True):
					self.CapturedsnarlCenterNose = y
				if (self.snarlActivated == True):
					self.snarlCenterNose = y
			elif (self.count == 42):
				if (self.captureFacePositions == True):
					self.CapturedsnarlEyeBotCenterLeft = y
				if (self.snarlActivated == True):
					self.snarlEyeBotCenterLeft = y
			elif (self.count == 48):
				if (self.captureFacePositions == True):
					self.CapturedsnarlEyeBotCenterRight = y
				if (self.snarlActivated == True):
					self.snarlEyeBotCenterRight = y							
			
			# right eyebrow
			elif (self.count == 25):
				if self.raiseEyebrowsActivated == True:
					self.EyebrowRight = y
					
				if (self.captureFacePositions == True):
					self.capturedEyebrowRight = y
						
			# left eye
			elif (self.count == 38): 
				if self.raiseEyebrowsActivated == True  or self.snarlActivated == True:
					self.EyeTopLeft = y
					
				if (self.captureFacePositions == True):
					self.capturedEyeTopLeft = y
					
			# right eye
			elif (self.count == 44):
				if self.raiseEyebrowsActivated == True  or self.snarlActivated == True:
					self.EyeTopRight = y
					
				if (self.captureFacePositions == True):
					self.capturedEyeTopRight = y
			# smile
			elif (self.count == 49):
				if (self.captureFacePositions == True):
					self.capturedLeftSideMouth = x	
					
				if self.smileActivated == True:
					self.LeftSideMouth = (x)
				
			elif (self.count == 55):
				if (self.captureFacePositions == True):
					self.capturedRightSideMouth = x
					
				if self.smileActivated == True:
					self.RightSideMouthSide = (x)
					
			# open mouth
			elif (self.count == 52):
				if (self.openMouthActivated == True):
					self.topMouth = y
					
				if (self.captureFacePositions == True):
					self.capturedTopMouth = y
					
			elif (self.count == 58):
				if (self.openMouthActivated == True):
					self.bottomMouth = y
					
				if (self.captureFacePositions == True):
					self.capturedBottomMouth = y

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		QApplication.setStyle(QtWidgets.QStyleFactory.create('native_style'))
		
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
		#QApplication.setPalette(dark_palette)

		self.setStyleSheet("QPushButton { background-color: gray; }\n"
              "QPushButton:enabled { background-color: green; }\n")
			  
		# Buttons 
		btnInitialize = QPushButton('activate', self)
		btnInitialize.setToolTip('activate face detection')
		btnInitialize.move(100, 460)
		btnInitialize.clicked.connect(self.on_click_initialize)

		btnCapture = QPushButton('revalue', self)
		btnCapture.setToolTip('used to capture the initial face array.')
		btnCapture.move(200, 460)
		btnCapture.clicked.connect(self.on_click_capture)

		# Webcam
		self.webcam = QLabel(self)
		self.webcam.setText("Webcam")
		self.webcam.move(10, 10)
		self.webcam.resize(800, 400)

		# CheckBoxes
		# Open Mouth
		self.cboxOpenMouth = QCheckBox("open mouth", self)
		self.cboxOpenMouth.move(30,500)
		self.cboxOpenMouth.resize(500,40)
		self.cboxOpenMouth.stateChanged.connect(lambda:self.btnState(self.cboxOpenMouth))
		# Raise Eyebrows
		self.cboxRaiseEyebrows = QCheckBox("raise eyebrows", self)
		self.cboxRaiseEyebrows.move(120,500)
		self.cboxRaiseEyebrows.resize(320,40)
		self.cboxRaiseEyebrows.stateChanged.connect(lambda:self.btnState(self.cboxRaiseEyebrows))
		# Smile
		self.cboxSmile = QCheckBox("smile",self)
		self.cboxSmile.move(230,500)
		self.cboxSmile.resize(320,40)
		self.cboxSmile.stateChanged.connect(lambda:self.btnState(self.cboxSmile))
		# Snarl
		self.cboxSnarl = QCheckBox("snarl",self)
		self.cboxSnarl.move(310,500)
		self.cboxSnarl.resize(320,40)
		self.cboxSnarl.stateChanged.connect(lambda:self.btnState(self.cboxSnarl))		
		
		# ComboBox
		# Open Mouth
		comboBox = QtWidgets.QComboBox(self)
		comboBox.addItem("a")
		comboBox.addItem("b")
		comboBox.move(100,550)
		
		comboBox.activated.connect( lambda index: self.style_choice(comboBox) )
		
		# Eyebrows
		comboBox2 = QtWidgets.QComboBox(self)
		comboBox2.addItem("a")
		comboBox2.addItem("b")
		comboBox2.move(190,550)
		
		comboBox2.activated.connect( lambda index: self.style_choice(comboBox2) )
		
		# Smile
		comboBox3 = QtWidgets.QComboBox(self)
		comboBox3.addItem("a")
		comboBox3.addItem("b")
		comboBox3.move(300,550)

		comboBox3.activated.connect( lambda index: self.style_choice(comboBox3) )

		# Smile
		comboBox4 = QtWidgets.QComboBox(self)
		comboBox4.addItem("a")
		comboBox4.addItem("b")
		comboBox4.move(380,550)

		comboBox4.activated.connect( lambda index: self.style_choice(comboBox4) )

		self.plaintxt = QPlainTextEdit(self)
		self.plaintxt.insertPlainText("You can write text here.\n")
		self.plaintxt.move(443, 463)
		self.plaintxt.resize(220, 130)
		
		self.show()
		
	def style_choice(self, text):
		if self.smiling == True:
			if (text == "a"):
				keyboard.press(Key.down)
				print('a')
			if (text == "b"):
				print("b")

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
	
	# this method captures the points of the face, to compare the differences between the values.
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