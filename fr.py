import sys 
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QWidget, QPushButton, QLabel, QPlainTextEdit, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from imutils import face_utils
import numpy as np
from collections import deque
import cv2
import dlib
# Used to insert keys
import win32com.client as comclt
import os
import pygame
#import psutil
import time

import json # for saving/loading settings

class App(QDialog):
	def __init__(self):
		super(App, self).__init__()
		self.title = 'FR'
		self.closeEvent = self.closeEvent
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.left = 200
		self.top = 200
		self.width = 910
		self.height = 420
		self.setWindowIcon(QtGui.QIcon('icon.png'))
		self.captureFacePositions = True
		self.capturedPositions = False
		self.faceShapePredictorActivated = False
		self.count = 0
		self.webcamActive = True
		# gives an error without CAP_DSHOW
		self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		pygame.init()
		self.initUI()
		self.smileActivated = False
		self.openMouthActivated = False
		self.raiseEyebrowsActivated = False
		self.snarlActivated = False
		self.blinkActivated = False
		# Open Notepad
		os.startfile('file.txt')
		self.wsh = comclt.Dispatch("WScript.Shell")
		# # Iterate over all running process
		# for proc in psutil.process_iter():
			# try:
				# # Get process name & pid from process object.
				# processName = proc.name()
				# processID = proc.pid
				# print(processName , ' ::: ', processID)
			# except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
				# pass
		self.center()
		self.oldPos = self.pos()
		self.landmarks()
		
		self.openMouthVar = 0.18
		self.raiseEyebrowsVar = 0.2
		self.smileVar = 0.3
		self.snarlVar = 0.354
		self.blinkVar = 0.046

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		delta = QPoint (event.globalPos() - self.oldPos)
		#print(delta)
		self.move(self.x() + delta.x(), self.y() + delta.y())
		self.oldPos = event.globalPos()
	
	def landmarks(self):
		# p = our pre-treined model directory, on my case, it's on the same script's directory.
		p = "shape_predictor_68_face_landmarks.dat"
		
		detector = dlib.get_frontal_face_detector()
		predictor = dlib.shape_predictor(p)

		gesture_arr = deque(maxlen=20)
		gesture_arr.extend([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
		
		def saveSettings(path, fileName, data):
			filePathNameWExt = './' + path + '/' + fileName + '.json'
			with open(filePathNameWExt, 'w') as fp:
				json.dump(data, fp)bb
		
		while self.webcamActive == True:
			# Getting out image by webcam 
			_, frame = self.cap.read()
			# Converting the image to gray scale
			if(frame is not None):
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				# Get faces into webcam's image
				rects = detector(gray, 0)
			else:
				print("Error connecting to webcam! Exiting...")
				sys.exit()
			#start_time = time.time() # start time of the loop
			
			# Activated
			if (self.faceShapePredictorActivated == True):
				for (i, rect) in enumerate(rects):
				
					start_time = time.time() # start time of the loop
					
					# Make the prediction and transfom it to numpy array
					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)
					
					# Green
					for (x, y) in shape:
						cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
					# Recognise gestures
					
					# Baseline
					base_line = ((shape[16][0]) - (shape[0][0]))
					
					# Open mouth
					if (self.openMouthActivated == True):
						mouth_top = ((shape[61][1]) + (shape[62][1]) + (shape[63][1]))/3
						mouth_bottom = ((shape[65][1]) + (shape[66][1]) + (shape[67][1]))/3
						mouth_height = mouth_bottom - mouth_top
						try:
							if(mouth_height/base_line > float(self.openMouthVar)):
								gesture_arr.append(0)
						except:
							pass
					# Raise Eyebrow
					if (self.raiseEyebrowsActivated == True):
						eye_top = ((shape[18][1]) + (shape[19][1]) + (shape[20][1]) + (shape[23][1]) + (shape[24][1]) + (shape[25][1]))/6
						eye_bottom = ((shape[27][1]) + (shape[28][1]))/2
						eye_height = eye_bottom - eye_top
						try:
							if(eye_height/base_line > float(self.raiseEyebrowsVar)):
								gesture_arr.append(1)
						except:
							pass
					# Blink
					if (self.blinkActivated == True):
						eyelid_top = ((shape[37][1]) + (shape[38][1]) + (shape[43][1]) + (shape[44][1]))/4
						eyelid_bottom = ((shape[40][1]) + (shape[41][1]) + (shape[46][1]) + (shape[47][1]))/4
						eyelid_height = eyelid_bottom - eyelid_top
						try:
							if(eyelid_height/base_line < float(self.blinkVar)):
								gesture_arr.append(2)
						except:
							pass
					# Smile
					if (self.smileActivated == True):
						mouth_left = ((shape[48][0]) + (shape[49][0]) + (shape[59][0]) + (shape[60][0]))/4
						mouth_right = ((shape[53][0]) + (shape[54][0]) + (shape[55][0]) + (shape[64][0]))/4
						mouth_width = mouth_right - mouth_left
						try:
							if(mouth_width/base_line > float(self.smileVar)):
								gesture_arr.append(3)
						except:
							pass
					# Scrunch nose
					if (self.snarlActivated == True):
						nose_top = ((shape[21][1]) + (shape[22][1]))/2
						nose_bottom = ((shape[31][1]) + (shape[35][1]))/2
						nose_height = nose_bottom - nose_top
						try:
							if(nose_height/base_line < float(self.snarlVar)):
								gesture_arr.append(4)
						except:
							pass
					
					gesture_output = max(set(gesture_arr), key=gesture_arr.count)
					
					if(gesture_output == 0):
						print("Mouth opened! - ",(mouth_height/base_line))
						
						for i in range(48, 68, 1):
							cv2.circle(frame, (shape[i][0], shape[i][1]), 2, (0, 0, 0), -1)
							
						self.wsh.AppActivate("Notepad") # select another application
						self.wsh.SendKeys(self.txtOpenMouth.toPlainText())
						
					elif(gesture_output == 1):
						print("Eyebrows raised! - ",(eye_height/base_line))
						
						self.wsh.AppActivate("Notepad") # select another application
						self.wsh.SendKeys(self.txtRaiseEyebrows.toPlainText())
						
					elif(gesture_output == 2):
						print("Eye close detected! - ",(eyelid_height/base_line))
						self.wsh.AppActivate("Notepad") # select another application
						self.wsh.SendKeys(self.txtBlink.toPlainText())
						
					elif(gesture_output == 3):
						print("Smile detected! - ",(mouth_width/base_line))
						self.wsh.AppActivate("Notepad") # select another application
						self.wsh.SendKeys(self.txtSmile.toPlainText())
						
					elif(gesture_output == 4):
						print("Anger detected! - ",(nose_height/base_line))
						self.wsh.AppActivate("Notepad") # select another application
						self.wsh.SendKeys(self.txtSnarl.toPlainText())
				
					if(gesture_output == 0 or gesture_output == 1 or gesture_output == 2 or gesture_output == 3 or gesture_output == 4):
						gesture_arr = deque(maxlen=20)
						gesture_arr.extend([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
						print(gesture_output)
						time.sleep(0.5)
						
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
				
			#print("FPS: ", float(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
				
		cv2.destroyAllWindows()
		self.cap.release()
		
	def wait_for_key(self):
		e = pygame.event.wait()
		while e.type != pygame.KEYDOWN:
			e = pygame.event.wait()
			if e.type == pygame.QUIT:
				return pygame.K_ESCAPE
		return e.key
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		loadUi('fr2.ui',self)
		
		# QApplication.setStyle(QtWidgets.QStyleFactory.create('native_style'))
		# # Introducing - The QPalette 
		# dark_palette = QPalette()
		# dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
		# dark_palette.setColor(QPalette.WindowText, Qt.red)
		# dark_palette.setColor(QPalette.Base, Qt.red)
		# dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		# dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
		# dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		# dark_palette.setColor(QPalette.Text, Qt.white)
		# dark_palette.setColor(QPalette.Button, Qt.red)
		# dark_palette.setColor(QPalette.ButtonText, Qt.white)
		# #dark_palette.setColor(QPalette.BRightSideMouthText, Qt.red)
		# dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		# dark_palette.setColor(QPalette.Highlight, Qt.white)
		# dark_palette.setColor(QPalette.HighlightedText, Qt.red)
		# QApplication.setPalette(dark_palette)
		# self.setStyleSheet("QPushButton { background-color: gray; }\n"
              # "QPushButton:enabled { background-color: red; }\n")

		self.cboxOpenMouth.stateChanged.connect(lambda:self.btnState(self.cboxOpenMouth))
		self.cboxRaiseEyebrows.stateChanged.connect(lambda:self.btnState(self.cboxRaiseEyebrows))
		self.cboxSmile.stateChanged.connect(lambda:self.btnState(self.cboxSmile))
		self.cboxSnarl.stateChanged.connect(lambda:self.btnState(self.cboxSnarl))	
		self.cboxBlink.stateChanged.connect(lambda:self.btnState(self.cboxBlink))
		
		# Buttons
		self.btnInitialize.setToolTip('activate face detection')
		self.btnInitialize.clicked.connect(self.on_click_initialize)		
		
		# Sliders
		self.sliderOpenMouth.valueChanged.connect(lambda:self.valuechanged())
		self.sliderRaiseEyebrows.valueChanged.connect(lambda:self.valuechanged())
		self.sliderSmile.valueChanged.connect(lambda:self.valuechanged())
		self.sliderSnarl.valueChanged.connect(lambda:self.valuechanged())
		self.sliderBlink.valueChanged.connect(lambda:self.valuechanged())
		
		qbtn = QPushButton('X', self)
		qbtn.clicked.connect(self.close)
		qbtn.resize(qbtn.sizeHint())
		qbtn.resize(30,20)
		qbtn.move(855, 10)
		
		# Webcam
		self.webcam.setText("Webcam")
		#self.webcam.move(10, 10)
		#self.webcam.resize(640, 480)
		self.show()

	def valuechanged(self):
		self.openMouthVar = float(self.sliderOpenMouth.value())/277
		self.raiseEyebrowsVar = float(self.sliderRaiseEyebrows.value())/250
		self.smileVar = float(self.sliderSmile.value())/166
		self.snarlVar = float(self.sliderSnarl.value())/141
		self.blinkVar = float(self.sliderBlink.value())/1070

		self.txtOpenMouthT = str(self.openMouthVar)
		self.txtRaiseEyebrowsT = str(self.raiseEyebrowsVar)
		self.txtSmileT = str(self.smileVar)
		self.txtSnarlT = str(self.snarlVar)
		self.txtBlinkT = str(self.blinkVar)
		
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
	
	def closeEvent(self, event):
		#print("event")
		reply = QMessageBox.question(self, 'Message',
			"Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

		if reply == QMessageBox.Yes:
			self.webcamActive = False
			event.accept()

		else:
			event.ignore()
	
app = QApplication(sys.argv)
widget = App()
widget.show()
pygame.quit()
print("Now exiting")
sys.exit()