from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
from threading import Thread
import subprocess
import atexit
import time
import sys
from progress.bar import Bar
# from modules.tk import ser, update_ser, rem_client
# from tkinter import *
import os


'''
try:
	port = int(sys.argv[1])
except Exception as e:
	port = 5050
host = ''
'''

clients = {}
senders = {}
addrs = {}
sender_add = {}

buff = 1024
addr = ()

# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server = socket(AF_INET, SOCK_STREAM)

j = 0
def incoming():
	i = 0
	global j
	while True:
		print("#"*30 + "\nLooking for connections...")
		client, client_addr = server.accept()						# waiting for connections
		print("%s:%s is running..." % client_addr)
		client.send(bytes("hello, you are live.", "utf8"))
		check = ""
		check = client.recv(buff).decode("utf8")		# receiving sender or reciever text for classification
		print("Connected a " + check)
		if check == "server":
			print("server up!")
			sender_add[client] = client_addr		# saving connected senders addr and info in sender_add[]
			j += 1
			senders[client] = "sender_" + str(j)				# save senders in list senders[]
			# update_ser(str(client_addr), "sen")
			Thread(target = handle_client, args = (client,j-1,)).start()
			print("server list updated:")						# Print sender list
			for x in senders:
				print(senders[x])
		else:
			print("client up!")
			addrs[client] = client_addr				# saving connected client addr and info in addrs[]
			i += 1
			clients[client] = "user_" + str(i)					# save clients in clients[] list
			# update_ser(str(client_addr), "rec")
			print("client list updated:")						# print clients list
			for x in clients:
				print(clients[x])
			
def handle_client(client, info):							# thread to handle senders
	print("Sender Server: ")
	f_flag = 0			#flag for file
	s_flag = 0			#flag for self
	#self_options = "1. for client list(type-> clients)\n2. for sender list(type-> senders)\n3. back to sending(type-> back)\n"
	while True:
		try:
			raw_msg = ""
			print("Threadx ~> waiting for msg...")
			raw_msg = client.recv(buff)
			print(raw_msg.decode("utf8"))
			
			if raw_msg.decode("utf8") == "file":
				file_proc(raw_msg, client)
				
			
			broadcast(raw_msg)
			if raw_msg.decode("utf8") == "quit":
				print("server closing")
				print(senders[client])
				client.close()
				
		except OSError:
			print("LOG: disconnecting afk sender: " + senders[client])
			print(info)
			# rem_client(info, "sen")
			client.close()
			del senders[client]
			exit()
			

def file_proc(raw, client):
	broadcast(raw)
	raw = ""
	raw = client.recv(buff)
	#broadcast(raw)
	file_bc(raw)
	info = ""
	name = ""
	size = ""
	info = raw.decode("utf8").split("#")
	name = info[1]
	size = int(info[2])
	
	if name == "fail":
		print("Error: File not received! Contact Adminstrator.")
		return 0
	
	while size:
		size -=1
		data = ""
		data = client.recv(buff)
		if not data:
			file_bc(data)
			break
		file_bc(data)
			
		
def broadcast(raw_msg):
	for sock in clients:
		try:
			sent = sock.send(bytes(raw_msg))							# why bytes here!
			if sent == 0:
				raise RuntimeError(clients[sock] + ">> socket conn broken in broadcast")
				ix = clients.index(sock)
				del clients[sock]
				# rem_client(ix, "rec")
		except Exception as e:
			print(e)
			raise RuntimeError(clients[sock] + ">> socket conn broken in broadcast")
			ix = clients.index(sock)
			del clients[sock]
			# rem_client(ix, "rec")
			
def file_bc(data):
	for sock in clients:
		try:
			sent = sock.send(data)
			if sent == 0:
				raise RuntimeError(clients[sock] + ">> socket conn broken during sending file <<")
				print("### removing afk - " + clients[sock])
				sock.close()
				ix = clients.index(sock)
				del clients[sock]
				# rem_client(ix, "rec")
		except OSError:
			print("removing afk - " + clients[sock])
			sock.close()
			ix = clients.index(sock)
			del clients[sock]
			# rem_client(ix, "rec")
		except Exception as e:
			#sock.close()
			print(e)
			ix = clients.index(sock)
			del clients[sock]
			# rem_client(ix, "rec")

'''	
def connec():				# done
	conn = Tk()
	conn.title("Lunching Server...")
	conn.geometry('280x220')
	f1 = Frame(conn)
	f1.pack()
	
	port = IntVar()
	port.set('')
	port_e = Entry(f1, textvariable = port)
	port_e.pack(side = BOTTOM)
	port_l = Label(f1, text = "Port No ")
	port_l.pack(side = BOTTOM)
	
	state = "Enter Port"
	conn_state = Label(conn, text = state)
	connect = Button(conn, text = "Server Up")
	quit = Button(conn, text = "Close")
	ip_add = ''
	port_no = ''
	def ip_port():
		global addr
		port_no = 5050
		
		if (port_no != ''):
			addr = ('', port_no)
			print(addr)
			state = "Starting server at port : " + str(port_no)
			# conn_state.config(text=state)
			#connect.config(state=DISABLED)
			c = connection()
			if c == 1:
				state = "Connection Failed, check port!"
				# conn_state.config(text=state)
			elif c == 0:
				#conn.destroy()
				pass
			
		else:
			print("Invalid Port!")
			state = "Invalid Port!"
			# conn_state.config(text=state)
		
	def qt():
		# conn.destroy()
		exit()	
	quit.pack(side=BOTTOM,pady=10)
	connect.pack(side=BOTTOM)
	connect.config(command=ip_port)
	quit.config(command = qt)
	conn_state.pack(pady=10)
	conn.mainloop()
'''
def connection(port):
	try:
		global server
		port_no = port
		addr = ('', port_no)
		server.bind(addr)
		print(addr)
		server.listen(5)
		# Thread(target = ser).start()
		return 0
	except Exception as e:
		print(e)
		return 1

def end_game():
	#for x in clients:
	#			x.close()
	#server.close()
	print("Game Over! h4x0r :-)")
	#for client in
	

#print("Server up")
#print(socket.gethostbyname(socket.gethostname()))
#print("on port no - " + str(port))			
#incoming()
connection(5050)
accept_thread = Thread(target = incoming)
accept_thread.start()
accept_thread.join()
atexit.register(end_game)
