from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
from tkinter import *
import subprocess
import time
import atexit
from pathlib import Path
from threading import Thread

host = input("ip addr: ")
port = input("port no: ")

buff = 1024
addr = (host, int(port))


print("connecting... " + str(addr))
c_sock = socket(AF_INET, SOCK_STREAM)
c_sock.connect(addr)
print("connected(check)")
c_sock.send(bytes("client", "utf8"))

def rec():
	flag = 0
	while True:
		try:
			print("waiting for msg...")
			msg = ""
			msg = c_sock.recv(buff).decode("utf8")
			"""if flag == 0:
				msg = raw_msg.decode("utf8")
			else:
				msg = raw_msg"""
			if msg and flag == 0:
				print("Display ~> " + msg)
				subprocess.run(["notify-send", msg])
				#display(msg)
			elif msg == '':
				raise RuntimeError("socket conn broken")
				c_sock.close()
				break
				
			if msg == "quit" and flag == 0:
				print("breaking out")
				c_sock.shutdown(SHUT_WR)
				#c_sock.close()
				#break
			if msg == "file":
				#flag = 1
				i = 0
				info = ""
				info = c_sock.recv(buff).decode("utf8")
				info = info.split("#")
				name = info[0]
				size = int(info[1])
				#size = int(c_sock.recv(buff).decode("utf8"))
				print("File receiving...")
				print("Name: " + name + "\nSize: " + str(size))
				if name != "fail":
					name = file_check(name)
					f = open(name, 'wb')
					while size:
						size -= 1
						data =""
						data = c_sock.recv(buff)
						#print("data = ", (data))
						i += 1
						print("receiving..." + str(i) + "...left..." + str(size))
						if not data:
							break
						f.write(data)
					f.close()
					Thread(target = open_file, args = (name,)).start()			# opening file using threads
					
					#c_sock.close()
					#break
				else:
					print("Error: File not received!")
					subprocess.run(["notify-send", "error: no file"])
		except OSError:
			print("error")
			c_sock.shutdown(SHUT_WR)
			c_sock.close()
			break
			
def display(msg):								# not working right now
	print(msg)
	root = Tk()
	root.overrideredirect(True)
	root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
	w = Label(root, text = "This is test.")
	w.pack()
	root.mainloop()

def file_check(name, i = 1):
	my_file = Path("./" + name)
	if my_file.is_file():
		name = file_check(ren(name))
	return name

def ren(name):
	rn = ""
	part = name.split(".")
	extn = part[len(part) - 1]
	for p in part:
		if p != extn:
			rn += p
	rn = rn + "x." + extn
	return rn			

def open_file(name):
	subprocess.run(["xdg-open", name])

def end_game():
	c_sock.close()

rec()
atexit.register(end_game)