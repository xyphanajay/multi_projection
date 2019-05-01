from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
from tkinter import *
import subprocess
import time

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
	while True:
		try:
			print("waiting for msg...")
			msg = c_sock.recv(buff).decode("utf8")
			
			if msg:
				print("Display ~> " + msg)
				subprocess.run(["notify-send", msg])
				#display(msg)
			elif msg == '':
				raise RuntimeError("socket conn broken")
				c_sock.close()
				break
				
			if msg == "quit":
				print("breaking out")
				c_sock.shutdown(SHUT_WR)
				#c_sock.close()
				#break
			if msg == "file":
				name = c_sock.recv(buff).decode("utf8")
				f = open(name, 'wb')
				data = c_sock.recv(buff)
				print("data = ", (data))
				if not data:
					break
				f.write(data)
				f.close()
				subprocess.run(["xdg-open", name])
				c_sock.close()
				break
		except OSError:
			print("error")
			c_sock.shutdown(SHUT_WR)
			c_sock.close()
			break
			
def display(msg):
	print(msg)
	root = Tk()
	root.overrideredirect(True)
	root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
	w = Label(root, text = "This is test.")
	w.pack()
	root.mainloop()


rec()