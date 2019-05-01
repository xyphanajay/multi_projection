from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
from threading import Thread
import subprocess
import atexit
import time

clients = {}
addrs = {}

host = ''
port = 5050
buff = 1024
addr = (host, port)

#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

server.listen(5)

def incoming():
	i = 0
	while True:
		print("#"*20 + "\nLooking for connections...")
		client, client_addr = server.accept()
		print("%s:%s is running..." % client_addr)
		client.send(bytes("hello, you are live.", "utf8"))
		#srvr = input("is it server? (y/n)")
		check = client.recv(buff).decode("utf8")
		print("got this ... " + check)
		if check == "server":
			print("server up!")
			#addrs[client] = client_addr
			Thread(target = handle_client, args = (client,)).start()
			print("Thread started!")
			break
		else:
			print("client up!")
			addrs[client] = client_addr
			i += 1
			clients[client] = "user_" + str(i)
			print("client list updated:")
			for x in clients:
				print(clients[x])
			
def handle_client(client):
	print("Sender Server: ")
	while True:
		print("Threadx ~> waiting for msg...")
		msg = client.recv(buff)
		print("Threadx ~> sending - " + msg.decode("utf8"))
		
		broadcast(msg)
		if msg.decode("utf8") == "quit":
			print("closing server(check)")
			client.close()
			for x in clients:
				x.shutdown(SHUT_WR)
				x.close()
				del clients[x]
			print("all clients down(check)")
			server.shutdown(SHUT_WR)
			server.close()
			print("connection dropped(check)")
			break	
			
		
def broadcast(msg):
	for sock in clients:
			sent = sock.send(bytes(msg))
			if sent == 0:
				raise RuntimeError(clients[sock] + ">> socket conn broken")
				del clients[sock]
			
def end_game():
	server.close()
	print("Game Over! h4x0r :-)")
	

print("Server up")
#print(socket.gethostbyname(socket.gethostname()))
print("on port no - " + str(port))			
#incoming()
accept_thread = Thread(target = incoming)
accept_thread.start()
accept_thread.join()
atexit.register(end_game)