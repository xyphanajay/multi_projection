from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
import subprocess
import time

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
				f = open(f_name, 'rb')
				part = bytes(f_name, "utf8")
				#part = f.read(1024)
				while part:
					c_sock.send(part)
					print("sent...", repr(part))
					part = f.read(1024)
				f.close()
				c_sock.close()
				break
		except OSError:
			print("error")
			c_sock.shutdown(SHUT_WR)
			c_sock.close()
			break


send()
