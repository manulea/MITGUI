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
		self.width = 850
		self.height = 420
		
		self.setWindowIcon(QtGui.QIcon('icon.png'))
		self.captureFacePositions = True
		self.capturedPositions = False
		self.faceShapePredictorActivated = False
		
		self.count = 0
		
		self.initUI()
				
		self.smileActivated = False
		self.openMouthActivated = False
		self.raiseEyebrowsActivated = False
		self.snarlActivated = False
		self.blinkActivated = False
				
		self.topLeftX = 0
		self.topLeftY = 0
		self.botRightX = 0
		self.botRightY = 0
		
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
			#	for (x, y) in T:
			#		cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
					
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

					count = 1

					for (x, y) in shape:
						self.leftRight(x, y, self.topLeftX, self.topLeftY, self.botRightX, self.botRightY, frame, self.count)
						self.count += 1

						#All points (Outline)
						cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
						# Eyebrows
						# if count > 17 and count < 28:
							# cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
						# Eyes
						# elif count > 36 and count < 49:
							# cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
						# Nose
						# elif count > 27 and count < 37:
							# cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
						# Mouth
						# elif count > 48:
							# cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
						
						count = count + 1
					# Recognise gestures
					# Baseline
					base_line = ((shape[16][0]) - (shape[0][0]))
					#print(base_line)
					# Open mouth
					#if (self.openMouthActivated == True):
					mouth_top = ((shape[61][1]) + (shape[62][1]) + (shape[63][1]))/3
					mouth_bottom = ((shape[65][1]) + (shape[66][1]) + (shape[67][1]))/3
					mouth_height = mouth_bottom - mouth_top
						
					if(mouth_height/base_line > 0.18):
						print("Mouth opened! - ",(mouth_height/base_line))
					
					# Raise Eyebrow
					if (self.raiseEyebrowsActivated == True):
						eye_top = ((shape[18][1]) + (shape[19][1]) + (shape[20][1]) + (shape[23][1]) + (shape[24][1]) + (shape[25][1]))/6
						eye_bottom = ((shape[27][1]) + (shape[28][1]))/2
						eye_height = eye_bottom - eye_top
						
						if(eye_height/base_line > 0.2):
							print("Eyebrows raised! - ",(eye_height/base_line))
					
					# Blink
					if (self.blinkActivated == True):
						eyelid_top = ((shape[37][1]) + (shape[38][1]) + (shape[43][1]) + (shape[44][1]))/4
						eyelid_bottom = ((shape[40][1]) + (shape[41][1]) + (shape[46][1]) + (shape[47][1]))/4
						eyelid_height = eyelid_bottom - eyelid_top
						
						if(eyelid_height/base_line < 0.0225):
							print("Blink detected! - ",(eyelid_height/base_line))
					
					# Smile
					if (self.smileActivated == True):
						mouth_left = ((shape[48][0]) + (shape[49][0]) + (shape[59][0]) + (shape[60][0]))/4
						mouth_right = ((shape[53][0]) + (shape[54][0]) + (shape[55][0]) + (shape[64][0]))/4
						mouth_width = mouth_right - mouth_left
						
						if(mouth_width/base_line > 0.34):
							print("Smile detected! - ",(mouth_width/base_line))
					
					# Scrunch nose
					if (self.snarlActivated == True):
						nose_top = ((shape[21][1]) + (shape[22][1]))/2
						nose_bottom = ((shape[31][1]) + (shape[35][1]))/2
						nose_height = nose_bottom - nose_top
						#print(nose_height/base_line)
						
						if(nose_height/base_line < 0.36):
							print("Anger detected! - ",(nose_height/base_line))

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
		QApplication.setPalette(dark_palette)

		self.setStyleSheet("QPushButton { background-color: gray; }\n"
              "QPushButton:enabled { background-color: green; }\n")

		# Webcam
		self.webcam = QLabel(self)
		self.webcam.setText("Webcam")
		self.webcam.move(10, 10)
		self.webcam.resize(800, 400)

		# CheckBoxes
		# Open Mouth
		self.cboxOpenMouth = QCheckBox("open mouth", self)
		self.cboxOpenMouth.move(670,90)
		self.cboxOpenMouth.resize(500,40)
		self.cboxOpenMouth.stateChanged.connect(lambda:self.btnState(self.cboxOpenMouth))
		
		# Raise Eyebrows
		self.cboxRaiseEyebrows = QCheckBox("raise eyebrows", self)
		self.cboxRaiseEyebrows.move(670,130)
		self.cboxRaiseEyebrows.resize(320,40)
		self.cboxRaiseEyebrows.stateChanged.connect(lambda:self.btnState(self.cboxRaiseEyebrows))
		
		# Smile
		self.cboxSmile = QCheckBox("smile",self)
		self.cboxSmile.move(670,170)
		self.cboxSmile.resize(320,40)
		self.cboxSmile.stateChanged.connect(lambda:self.btnState(self.cboxSmile))
		
		# Snarl
		self.cboxSnarl = QCheckBox("snarl",self)
		self.cboxSnarl.move(670,210)
		self.cboxSnarl.resize(320,40)
		self.cboxSnarl.stateChanged.connect(lambda:self.btnState(self.cboxSnarl))		
		
		# Blink
		self.cboxBlink = QCheckBox("blink",self)
		self.cboxBlink.move(670,250)
		self.cboxBlink.resize(320,40)
		self.cboxBlink.stateChanged.connect(lambda:self.btnState(self.cboxBlink))	
		
		# ComboBox
		# Open Mouth
		#comboBox = QtWidgets.QComboBox(self)
		#comboBox.addItem("a")
		#comboBox.addItem("b")
		#comboBox.move(30,550)
		self.txtOpenMouth = QPlainTextEdit(self)
		self.txtOpenMouth.insertPlainText("")
		self.txtOpenMouth.move(780, 100)
		self.txtOpenMouth.resize(50, 25)
		
		#comboBox.activated.connect( lambda index: self.style_choice(comboBox) )
		
		# Eyebrows
		#comboBox2 = QtWidgets.QComboBox(self)
		#comboBox2.addItem("a")
		#comboBox2.addItem("b")
		#comboBox2.move(190,550)
		#comboBox2.activated.connect( lambda index: self.style_choice(comboBox2) )
		self.txtRaiseEyebrows = QPlainTextEdit(self)
		self.txtRaiseEyebrows.insertPlainText("")
		self.txtRaiseEyebrows.move(780, 140)
		self.txtRaiseEyebrows.resize(50, 25)
		
		# Smile
		#comboBox3 = QtWidgets.QComboBox(self)
		#comboBox3.addItem("a")
		#comboBox3.addItem("b")
		#comboBox3.move(300,550)
		#comboBox3.activated.connect( lambda index: self.style_choice(comboBox3) )
		self.txtSmile = QPlainTextEdit(self)
		self.txtSmile.insertPlainText("")
		self.txtSmile.move(780, 180)
		self.txtSmile.resize(50, 25)

		# Snarl
		#comboBox4 = QtWidgets.QComboBox(self)
		#comboBox4.addItem("a")
		#comboBox4.addItem("b")
		#comboBox4.move(380,550)
		#comboBox4.activated.connect( lambda index: self.style_choice(comboBox4) )
		self.txtSnarl = QPlainTextEdit(self)
		self.txtSnarl.insertPlainText("")
		self.txtSnarl.move(780, 220)
		self.txtSnarl.resize(50, 25)
		
		# Blink
		self.txtSnarl = QPlainTextEdit(self)
		self.txtSnarl.insertPlainText("")
		self.txtSnarl.move(780, 260)
		self.txtSnarl.resize(50, 25)
		
		# Buttons
		btnInitialize = QPushButton('activate', self)
		btnInitialize.setToolTip('activate face detection')
		btnInitialize.move(670, 330)
		btnInitialize.clicked.connect(self.on_click_initialize)

		btnCapture = QPushButton('revalue', self)
		btnCapture.setToolTip('used to capture the initial face array.')
		btnCapture.move(755, 330)
		btnCapture.clicked.connect(self.on_click_capture)
		
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
				
		# blink checkbox
		if state.text() == "blink":
			if state.isChecked() == True:
				if (self.blinkActivated == False):
					print("blink detection activated")
					self.blinkActivated = True
			else:
				self.blinkActivated = False
				print("blink detection deactivated")
		
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