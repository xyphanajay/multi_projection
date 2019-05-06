from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
from threading import Thread
import subprocess
import atexit
import time

clients = {}
senders = {}
addrs = {}
sender_add = {}


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
	j = 0
	while True:
		print("#"*30 + "\nLooking for connections...")
		client, client_addr = server.accept()								# waiting for connections
		print("%s:%s is running..." % client_addr)
		client.send(bytes("hello, you are live.", "utf8"))
		check = ""
		check = client.recv(buff).decode("utf8")							# receiving sender or reciever text for classification
		print("Connected a " + check)
		if check == "server":
			print("server up!")
			sender_add[client] = client_addr								# saving connected senders addr and info in sender_add[]
			j += 1
			senders[client] = "sender_" + str(j)							# save senders in list senders[]
			Thread(target = handle_client, args = (client,)).start()		# create THREAD to handle senders
			print("server list updated:")									# Print sender list
			for x in senders:
				print(senders[x])
		else:
			print("client up!")
			addrs[client] = client_addr										# saving connected client addr and info in addrs[]
			i += 1
			clients[client] = "user_" + str(i)								# save clients in clients[] list
			print("client list updated:")									# print clients list
			for x in clients:
				print(clients[x])
			
def handle_client(client):													# thread to handle senders
	print("Sender Server: ")
	f_flag = 0			#flag for file
	s_flag = 0			#flag for self
	self_options = "1. for client list(type-> clients)\n2. for sender list(type-> senders)\n3. back to sending(type-> back)\n"
	while True:
		try:
			raw_msg = ""
			print("Threadx ~> waiting for msg...")
			raw_msg = client.recv(buff)
			print(raw_msg.decode("utf8"))
			if raw_msg.decode("utf8") == "file":
				broadcast(raw_msg)					# send file as text 
				raw_msg = ""
				raw_msg = client.recv(buff)
				broadcast(raw_msg)		# send file name and size as text
				info = ""
				info = raw_msg.decode("utf8").split("#")
				size = int(info[1])
				#broadcast(client.recv(buff))		# send size of file
				#f_flag = 1
				while size:
					size -= 1
					data = ""
					data = client.recv(buff)
					#print("data = ", (data))
					print("receiving..." + str(size))
					if not data:
						break
					file_bc(data)
		
			
			broadcast(raw_msg)
			if raw_msg.decode("utf8") == "quit":
				print("server closing")
				print(senders[client])
				client.close()
		except OSError:
			print("disconnecting akf sender: " + senders[client])
			client.close()
			del senders[client]
			
			"""for x in clients:
				x.shutdown(SHUT_WR)
				x.close()
				del clients[x]
			print("all clients down(check)")
			server.shutdown(SHUT_WR)
			server.close()
			print("connection dropped(check)")
			break"""	

"""
File "cute_server.py", line 57, in handle_client
    for x in clients:
RuntimeError: dictionary changed size during iteration	
"""
		
def broadcast(raw_msg):
	for sock in clients:
		sent = sock.send(bytes(raw_msg))							# why bytes here!
		if sent == 0:
			raise RuntimeError(clients[sock] + ">> socket conn broken")
			del clients[sock]
			
def file_bc(data):
	for sock in clients:
		try:
			sent = sock.send(data)
			if sent == 0:
				raise RuntimeError(clients[sock] + ">> socket conn broken <<")
				print("### removing afk - " + clients[sock])
				sock.close()
				del clients[sock]
		except OSError:
			print("removing afk - " + clients[sock])
			sock.close()
			del clients[sock]
			
def end_game():
	#for x in clients:
	#			x.close()
	#server.close()
	print("Game Over! h4x0r :-)")
	

print("Server up")
#print(socket.gethostbyname(socket.gethostname()))
print("on port no - " + str(port))			
#incoming()
accept_thread = Thread(target = incoming)
accept_thread.start()
accept_thread.join()
atexit.register(end_game)