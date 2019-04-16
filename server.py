#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM #for TCP socket AF_INET SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = ''
PORT = 5050
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
	"""TO HANDLE INCOMING CONNECTION"""
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		client.send(bytes("Yo niggers!" + "who are you!", "utf8"))
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
	"""takes client socket as arg - HANDLES A CLIENT CONN"""
	name = client.recv(BUFSIZ).decode("utf8")
	welc = 'Nailed it! quit -> {quit}' %name
	client.send(bytes(welcome, "utf8"))
	msg = "%s is ready to roll!" %name
	broadcast(bytes(msg, "utf8"))
	clients[client] = name
	while True:
		msg = client.recv(BUFSIZ)
		if msg != bytes("{quit}", "utf8"):
			broadcast(msg, name + ": ")
		else:
			client.send(bytes("{quit}", "utf8"))
			client.close()
			del clients[client]
			broadcast(bytes("%s went rouge!!" %name, "utf8"))
			break

def broadcast(msg, prefix = ""):	#prefix -> name id
	"""BROADCASTS MSG TO ALL CLIENTS"""
	for sock in clients:
		sock.send(bytes(prefix, "utf8") + msg)

if __name__ == "__main__":
	SERVER.listen(5) #max 5 connections
	print("waiting for niggers!!!")
	ACCEPT_THREAD = Thread(target = accept_incoming_connections)
	ACCEPT_THREAD.start()	#starts infinite loop
	ACCEPT_THREAD.join()
	SERVER.close()