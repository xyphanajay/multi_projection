from socket import AF_INET, socket, SOCK_STREAM
import subprocess

host = input("server ip: ")
port = input("port no: ")

buff = 1024
addr = (host, int(port))

c_sock = socket(AF_INET, SOCK_STREAM)
c_sock.connect(addr)

def send():
	while True:
		try:
			msg = input()
			print("sending: " + msg)
			c_sock.send(bytes(msg, "utf8"))
			if msg == "quit":
				c_sock.close()
				break
			#c_sock.close()
			#break
		except OSError:
			c_sock.close()
			break


send()
