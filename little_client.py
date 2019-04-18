from socket import AF_INET, socket, SOCK_STREAM
import subprocess

host = input("ip addr: ")
port = input("port no: ")

buff = 1024
addr = (host, int(port))

print("connecting... " + str(addr))
c_sock = socket(AF_INET, SOCK_STREAM)
c_sock.connect(addr)

def rec():
	while True:
		try:
			msg = c_sock.recv(buff).decode("utf8")
			if msg:
				subprocess.run(["notify-send", msg])
			#print(msg)
			if msg == "quit":
				print("breaking out")
				c_sock.close()
				break
		except OSError:
			c_sock.close()
			break
			
rec()