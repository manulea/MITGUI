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
from collections import deque

import cv2
import dlib

import win32com.client as comclt

import os

class App(QWidget):
	def __init__(self):
		super().__init__()

		self.title = 'Face Recognition'
		
		self.left = 200
		self.top = 200
		self.width = 910
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
		
		os.startfile('file.txt')

		self.landmarks()
		
	def push(a, n):
		a = np.roll(a, 1)
		a[0] = n
		return a
		
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
		
		gesture_arr = deque(maxlen=15)
		gesture_arr.extend([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
		
		while True:
			# Getting out image by webcam 
			_, frame = cap.read()
			# Converting the image to gray scale
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				
			# Get faces into webcam's image
			rects = detector(gray, 0)
			
			if (self.faceShapePredictorActivated == False):
				for (x, y) in T:
					cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
					
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
						cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
						count = count + 1
						
					# Recognise gestures
					
					# Baseline
					base_line = ((shape[16][0]) - (shape[0][0]))
					
					# Open mouth
					if (self.openMouthActivated == True):
						mouth_top = ((shape[61][1]) + (shape[62][1]) + (shape[63][1]))/3
						mouth_bottom = ((shape[65][1]) + (shape[66][1]) + (shape[67][1]))/3
						mouth_height = mouth_bottom - mouth_top
						
						try:
							if(mouth_height/base_line > float(self.txtOpenMouthT.toPlainText())):
								#print("Mouth opened! - ",(mouth_height/base_line))
								gesture_arr.append(0)
								#wsh = comclt.Dispatch("WScript.Shell")
								#wsh.AppActivate("Notepad") # select another application
								#wsh.SendKeys(self.txtOpenMouth.toPlainText())
						except:
							pass
						
					
					# Raise Eyebrow
					if (self.raiseEyebrowsActivated == True):
						eye_top = ((shape[18][1]) + (shape[19][1]) + (shape[20][1]) + (shape[23][1]) + (shape[24][1]) + (shape[25][1]))/6
						eye_bottom = ((shape[27][1]) + (shape[28][1]))/2
						eye_height = eye_bottom - eye_top
						
						try:
							if(eye_height/base_line > float(self.txtRaiseEyebrowsT.toPlainText())):
								gesture_arr.append(1)
								#print("Eyebrows raised! - ",(eye_height/base_line))
								#wsh = comclt.Dispatch("WScript.Shell")
								#wsh.AppActivate("Notepad") # select another application
								#wsh.SendKeys(self.txtRaiseEyebrows.toPlainText())
						except:
							pass
					
					# Blink
					if (self.blinkActivated == True):
						eyelid_top = ((shape[37][1]) + (shape[38][1]) + (shape[43][1]) + (shape[44][1]))/4
						eyelid_bottom = ((shape[40][1]) + (shape[41][1]) + (shape[46][1]) + (shape[47][1]))/4
						eyelid_height = eyelid_bottom - eyelid_top
						
						try:
							if(eyelid_height/base_line < float(self.txtBlinkT.toPlainText())):
								gesture_arr.append(2)
								#print("Blink detected! - ",(eyelid_height/base_line))
								#wsh = comclt.Dispatch("WScript.Shell")
								#wsh.AppActivate("Notepad") # select another application
								#wsh.SendKeys(self.txtBlink.toPlainText())
						except:
							pass
							
					# Smile
					if (self.smileActivated == True):
						mouth_left = ((shape[48][0]) + (shape[49][0]) + (shape[59][0]) + (shape[60][0]))/4
						mouth_right = ((shape[53][0]) + (shape[54][0]) + (shape[55][0]) + (shape[64][0]))/4
						mouth_width = mouth_right - mouth_left
						
						try:
							if(mouth_width/base_line > float(self.txtSmileT.toPlainText())):
								gesture_arr.append(3)
								#print("Smile detected! - ",(mouth_width/base_line))
								#wsh = comclt.Dispatch("WScript.Shell")
								#wsh.AppActivate("Notepad") # select another application
								#wsh.SendKeys(self.txtSmile.toPlainText())
						except:
							pass
					
					# Scrunch nose
					if (self.snarlActivated == True):
						nose_top = ((shape[21][1]) + (shape[22][1]))/2
						nose_bottom = ((shape[31][1]) + (shape[35][1]))/2
						nose_height = nose_bottom - nose_top
						#print(nose_height/base_line)
						try:
							if(nose_height/base_line < float(self.txtSnarlT.toPlainText())):
								gesture_arr.append(4)
								#print("Anger detected! - ",(nose_height/base_line))
								#wsh = comclt.Dispatch("WScript.Shell")
								#wsh.AppActivate("Notepad") # select another application
								#wsh.SendKeys(self.txtSnarl.toPlainText())
						except:
							pass
					
					gesture_output = max(set(gesture_arr), key=gesture_arr.count)
					
					if(gesture_output == 0):
						print("Mouth opened! - ",(mouth_height/base_line))
						wsh = comclt.Dispatch("WScript.Shell")
						wsh.AppActivate("Notepad") # select another application
						wsh.SendKeys(self.txtOpenMouth.toPlainText())
					elif(gesture_output == 1):
						print("Eyebrows raised! - ",(eye_height/base_line))
						wsh = comclt.Dispatch("WScript.Shell")
						wsh.AppActivate("Notepad") # select another application
						wsh.SendKeys(self.txtRaiseEyebrows.toPlainText())
					elif(gesture_output == 2):
						print("Eye close detected! - ",(eyelid_height/base_line))
						wsh = comclt.Dispatch("WScript.Shell")
						wsh.AppActivate("Notepad") # select another application
						wsh.SendKeys(self.txtBlink.toPlainText())
					elif(gesture_output == 3):
						print("Smile detected! - ",(mouth_width/base_line))
						wsh = comclt.Dispatch("WScript.Shell")
						wsh.AppActivate("Notepad") # select another application
						wsh.SendKeys(self.txtSmile.toPlainText())
					elif(gesture_output == 4):
						print("Anger detected! - ",(nose_height/base_line))
						wsh = comclt.Dispatch("WScript.Shell")
						wsh.AppActivate("Notepad") # select another application
						wsh.SendKeys(self.txtSnarl.toPlainText())
				
				if(gesture_output == 0 or gesture_output == 1 or gesture_output == 2 or gesture_output == 3 or gesture_output == 4):
					gesture_arr = deque(maxlen=20)
					gesture_arr.extend([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

			rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			image = QImage(rgb_frame.tobytes(), 
			rgb_frame.shape[1],
			rgb_frame.shape[0],
			QImage.Format_RGB888)
			
			self.webcam.setPixmap(QPixmap.fromImage(image))
			self.webcam.show()
			
			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				self.exit()
			# Press 'q' to break out of loop
			if cv2.waitKey(1) & 0xFF == ord('q'):
				self.exit()
				
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
		dark_palette.setColor(QPalette.WindowText, Qt.red)
		dark_palette.setColor(QPalette.Base, Qt.red)
		dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
		dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		dark_palette.setColor(QPalette.Text, Qt.white)
		dark_palette.setColor(QPalette.Button, Qt.red)
		dark_palette.setColor(QPalette.ButtonText, Qt.white)
		#dark_palette.setColor(QPalette.BRightSideMouthText, Qt.red)
		dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.Highlight, Qt.white)
		dark_palette.setColor(QPalette.HighlightedText, Qt.red)
		QApplication.setPalette(dark_palette)

		self.setStyleSheet("QPushButton { background-color: gray; }\n"
              "QPushButton:enabled { background-color: red; }\n")

		# Webcam
		self.webcam = QLabel(self)
		self.webcam.setText("Webcam")
		self.webcam.move(10, 10)
		self.webcam.resize(800, 400)	
		
		# Open Mouth	
		self.cboxOpenMouth = QCheckBox("open mouth", self)
		self.cboxOpenMouth.move(670,90)
		self.cboxOpenMouth.resize(500,40)
		self.cboxOpenMouth.stateChanged.connect(lambda:self.btnState(self.cboxOpenMouth))
		
		self.txtOpenMouth = QPlainTextEdit(self)
		self.txtOpenMouth.insertPlainText("a")
		self.txtOpenMouth.move(780, 100)
		self.txtOpenMouth.resize(50, 25)
		
		self.txtOpenMouthT = QPlainTextEdit(self)
		self.txtOpenMouthT.insertPlainText("0.18")
		self.txtOpenMouthT.move(835, 100)
		self.txtOpenMouthT.resize(50, 25)
		
		# Eyebrows
		self.cboxRaiseEyebrows = QCheckBox("raise eyebrows", self)
		self.cboxRaiseEyebrows.move(670,130)
		self.cboxRaiseEyebrows.resize(320,40)
		self.cboxRaiseEyebrows.stateChanged.connect(lambda:self.btnState(self.cboxRaiseEyebrows))
		
		self.txtRaiseEyebrows = QPlainTextEdit(self)
		self.txtRaiseEyebrows.insertPlainText("b")
		self.txtRaiseEyebrows.move(780, 140)
		self.txtRaiseEyebrows.resize(50, 25)
		
		self.txtRaiseEyebrowsT = QPlainTextEdit(self)
		self.txtRaiseEyebrowsT.insertPlainText("0.2")
		self.txtRaiseEyebrowsT.move(835, 140)
		self.txtRaiseEyebrowsT.resize(50, 25)
		
		# Smile
		self.cboxSmile = QCheckBox("smile",self)
		self.cboxSmile.move(670,170)
		self.cboxSmile.resize(320,40)
		self.cboxSmile.stateChanged.connect(lambda:self.btnState(self.cboxSmile))
		
		self.txtSmile = QPlainTextEdit(self)
		self.txtSmile.insertPlainText("c")
		self.txtSmile.move(780, 180)
		self.txtSmile.resize(50, 25)
		
		self.txtSmileT = QPlainTextEdit(self)
		self.txtSmileT.insertPlainText("0.3")
		self.txtSmileT.move(835, 180)
		self.txtSmileT.resize(50, 25)

		# Snarl
		self.cboxSnarl = QCheckBox("snarl",self)
		self.cboxSnarl.move(670,210)
		self.cboxSnarl.resize(320,40)
		self.cboxSnarl.stateChanged.connect(lambda:self.btnState(self.cboxSnarl))	
		
		self.txtSnarl = QPlainTextEdit(self)
		self.txtSnarl.insertPlainText("d")
		self.txtSnarl.move(780, 220)
		self.txtSnarl.resize(50, 25)
		
		self.txtSnarlT = QPlainTextEdit(self)
		self.txtSnarlT.insertPlainText("0.354")
		self.txtSnarlT.move(835, 220)
		self.txtSnarlT.resize(50, 25)
		
		# Blink	
		self.cboxBlink = QCheckBox("blink",self)
		self.cboxBlink.move(670,250)
		self.cboxBlink.resize(320,40)
		self.cboxBlink.stateChanged.connect(lambda:self.btnState(self.cboxBlink))	
		
		self.txtBlink = QPlainTextEdit(self)
		self.txtBlink.insertPlainText("e")
		self.txtBlink.move(780, 260)
		self.txtBlink.resize(50, 25)
		
		self.txtBlinkT = QPlainTextEdit(self)
		self.txtBlinkT.insertPlainText("0.046")
		self.txtBlinkT.move(835,260)
		self.txtBlinkT.resize(50,25)
		
		# Buttons
		self.btnInitialize = QPushButton('Activate', self)
		self.btnInitialize.setToolTip('activate face detection')
		self.btnInitialize.resize(110, 30)
		self.btnInitialize.move(700, 330)
		self.btnInitialize.clicked.connect(self.on_click_initialize)
		
		self.show()

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
			self.btnInitialize.setText("Activate")
			
		elif self.faceShapePredictorActivated == False:
			self.faceShapePredictorActivated = True
			self.btnInitialize.setText("Deactivate")
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	GUI = App()
	#GUI.show()
	sys.exit(app.exec_())