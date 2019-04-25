import RPi.GPIO as GPIO
import time
import threading
import os
import sys
from time import sleep


# GPIO.setup(18,GPIO.OUT)
# print "LED on"
# GPIO.output(18,GPIO.HIGH)
# time.sleep(1)
# print "LED off"
# GPIO.output(18,GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# class 

class Led:
	def __init__(self, pin):
		self.pin = pin
		self.isOn = False

		# GPIO.setmode( GPIO.BOARD) 
		GPIO.setup(self.pin, GPIO.OUT)
		self.pwm = GPIO.PWM(self.pin, 70)
		self.pwm.start(10) 

	def on(self):
		self.pwm.ChangeDutyCycle(100)
		# GPIO.output(self.pin, GPIO.HIGH)
		self.isOn = True

	def off(self):
		self.pwm.ChangeDutyCycle(0)
		GPIO.output(self.pin, GPIO.LOW)
		self.isOn = False

	def toggle(self):
		if self.isOn:
			self.off()
		else:
			self.on()

	def opacity(self, nr):
		self.pwm.ChangeDutyCycle(nr)

blue 	= Led(19)
green 	= Led(13)
red 	= Led(26)

global redOpacity
global greenOpacity
global blueOpacity

# white
red.opacity(55)
green.opacity(100)
blue.opacity(100)


while True:
	op = input()
	red.opacity(float(op))

# self.ui = threading.Thread(target=self.interface)
# self.ui.start()
