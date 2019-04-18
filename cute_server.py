from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import subprocess

clients = {}
addrs = {}

host = ''
port = 33333
buff = 1024
addr = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

server.listen(2)

def incoming():
	i = 0
	while True:
		client, client_addr = server.accept()
		print("%s:%s is up." % client_addr)
		client.send(bytes("hello, you are up.", "utf8"))
		srvr = input("is it server? (y/n)")
		if srvr == "y":
			print("server up!")
			#addrs[client] = client_addr
			Thread(target = handle_client, args = (client,)).start()
			#break
		else:
			print("client up!")
			addrs[client] = client_addr
			i += 1
			clients[client] = "user_" + str(i)
			
def handle_client(client):
	while True:
		msg = client.recv(buff)
		for sock in clients:
			sock.send(bytes(msg))
		if msg == "quit":
			client.close()
			break	
			

print("Server up")
#print(subprocess.run(["ifconfig", "|grep", "netmask"]))
print("on port no - " + str(port))			
incoming()