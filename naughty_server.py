from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
import subprocess
import time
import atexit
from pathlib import Path



host = input("server ip: ")
port = input("port no: ")

buff = 1024
addr = (host, int(port))

c_sock = socket(AF_INET, SOCK_STREAM)
c_sock.connect(addr)
print("connected(check)")
c_sock.send(bytes("server", "utf8"))

def send():
	while True:
		try:
			msg = input("~> ")
			print("<< " + msg)
			sent = c_sock.send(bytes(msg, "utf8"))
			if sent == 0:
				raise RuntimeError("socket connection broken")
				c_sock.close()
				break
			if msg == "quit":
				c_sock.shutdown(SHUT_WR)
				c_sock.close()
				break
			if msg == "file":
					
				f_name = input("File Name: ")
				my_file = Path("./" + f_name)
				if my_file.is_file():
					f = open(f_name, 'rb').read()
					size = len(f)
					s = int(size/1024) + 1
					info = f_name + "#" + str(s)
					print(info)
					part = bytes(info, "utf8")
					#part = f.read(1024)
					#while part:
					
					c_sock.send(part)					# sending file name
					#c_sock.send(bytes(str(s), "utf8"))		# sending size of file---- can receive in these many 1024 pkts
						#print("sent", repr(part))
					part = f
					c_sock.send(part)					# sending file
					print("sending..." + str(len(part)))
					#c_sock.send(bytes("", "utf8"))
					#f.close()
					#c_sock.close()
					#break
				else:
					c_sock.send(bytes("fail#0", "utf8"))
					print("Error: File not found!\nGoing back to text send mode.")
				c_sock.send(bytes("", "utf8"))
					
		except OSError:
			print("error")
			c_sock.shutdown(SHUT_WR)
			c_sock.close()
			break
		
			

def end_game():
	c_sock.close()

send()
atexit.register(end_game)