from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
import subprocess
import time
import atexit
from pathlib import Path
from modules.feature import cfile, streak	# to check file 
import sys
from tkinter import *
from random import random
'''
try:
	host = sys.argv[1]
except Exception as e:
	host = input("server ip: ")
try:
	port = sys.argv[2]
except Exception as e:
	port = input("port no: ")

c_sock = socket(AF_INET, SOCK_STREAM)
c_sock.connect(addr)
print("connected(check)")
c_sock.send(bytes("server", "utf8"))
'''
prior = 0
msg = ''
buff = 1024
addr = ()
c_sock = socket(AF_INET, SOCK_STREAM)


def send_msg(data, flag):
	msg = data
	try:
		#msg = input("~> ")
		print("<< " + msg)
		if flag == 0:
			sent = c_sock.send(bytes(msg, "utf8"))
			if sent == 0:
				raise RuntimeError("socket connection broken")
				c_sock.close()
				#break
			if msg == "quit":
				c_sock.shutdown(SHUT_WR)
				c_sock.close()
				#break
		elif flag == 10:
			sent = c_sock.send(bytes('file', "utf8"))
			file_send(msg, 0)	
		elif flag == 11:
			sent = c_sock.send(bytes('file', "utf8"))
			file_send(msg, 1)
	except OSError:
		print("error")
		c_sock.shutdown(SHUT_WR)
		c_sock.close()
		#break


def sender():
	
	send = Tk()
	send.title("Sender Portal")
	send.geometry('280x350')
	fr = Frame(send)
	fr.pack()
	
	close = Button(fr, text = "Quit", width = 10)
	close.pack(side = BOTTOM, pady=10)
	sbut = Button(fr, text = "Send", width = 10)
	sbut.pack(side=BOTTOM, pady = 10)
	state = Label(fr, text = "Type message and click send")
	state.pack(side=BOTTOM)
	f = IntVar()
	p = IntVar()
	p1 = Radiobutton(fr, text="Top", variable = p, value = 0)
	p2 = Radiobutton(fr, text="Low", variable = p, value = 1)
	
	def rad():
		#print("rad called")
		#print(f.get())
		x = f.get()
		if x == 0:
			state.config(text = "Type message and click send")
			p1.config(state= DISABLED)
			p2.config(state= DISABLED)
			
		elif x == 1:
			state.config(text = "Type path of file & click send")
			p1.config(state= 'normal')
			p2.config(state= 'normal')
	
	def qt():
		send_msg("quit", 0)
		send.destroy()
		exit()
	
	head = Label(fr, text = "Choose an option:")
	head.pack(side=TOP, pady = 10)
	r1 = Radiobutton(fr, text="Text Message", variable = f, value = 0, command = rad)
	r1.pack(anchor=W)
	r2 = Radiobutton(fr, text="File", variable = f, value = 1, command = rad)
	r2.pack(anchor=W)
	
	pr = Label(fr, text = "Choose priority of file:")
	pr.pack()
	pr2 = Label(fr, text = "(Text message priority: Top alawys)")
	pr2.pack()
	p1.pack(anchor=W)
	p2.pack(anchor=W)
	p1.config(state= DISABLED)
	p2.config(state= DISABLED)
	
	txt = StringVar() 
	text = Entry(fr, textvariable = txt)
	text.place(width=20, height=20)
	text.pack(pady=10)
	
	def s_button():
		global msg
		msg = txt.get()
		txt.set('')
		print(msg)
		print(f.get())
		if msg != '':
			magic = (f.get()*10) + p.get()
			send_msg(msg, magic)				#call sender
			r1.select()
			p1.select()
			p1.config(state= DISABLED)
			p2.config(state= DISABLED)
			f.set(0)
			p.set(0)
			
		else:
			state.config(text = "Type something and click send")
	close.config(command = qt)	
	sbut.config(command=s_button)
	send.mainloop()


def file_send(f_path, prior):
	f_name = f_path
	#f_name = input("File Name with location: ")	# expected file names - /home/file.txt ./file.name
	#prior = input("Priority lvl\n0 (high) to 5 (low): ")
	if prior == "":
		prior = 0
	my_file = Path(f_name)
	
	if cfile(my_file):				# checking file existence 
		#r1.select()
		print("ERROR: invalid file found! check file name. (can't send dir)")
		c_sock.send(bytes("#fail#0#5#", "utf8"))
		print("***going back to text mode***")
		return 0
		
	f = open(f_name, 'rb').read()		# opening file - ex /home/file.txt
	f_name = f_name.split('/')
	size = len(f)
	s = int(size/1024) + 1
	key = int(random() * 100) % 64			# generating key
	info = '#' + f_name[-1] + '#' + str(s) + '#' + str(prior) + '#' + str(key) + "#"
	print("sending info ... " + info)
	part = bytes(info, "utf8")
	time.sleep(1)					# sleep 1 sec
	c_sock.send(part)				# sending file info
	''''
							#xor implementation
	fo = open(f_name, 'rb')
	image = fo.read()
	fo.close()

	image = bytearray(image)
	for index, value in enumerate(image):
		image[index] = value^i_key
	'''
	part = f
	time.sleep(2)					# sleep 2 sec
	c_sock.send(part)				# sending file
	print("sending file ... " + str(len(part)))
	#f.close()
	return 0


def connec():				# done
	conn = Tk()
	conn.title("Connecting...")
	conn.geometry('280x220')
	f1 = Frame(conn)
	f1.pack()
	
	ip_l = Label(f1, text = "Server IP ")
	ip_l.pack(side=TOP)
	ip = StringVar()
	ip_e = Entry(f1,textvariable = ip)
	ip_e.pack(side=TOP)
	
	port = IntVar()
	port.set('')
	port_e = Entry(f1, textvariable = port)
	port_e.pack(side = BOTTOM)
	port_l = Label(f1, text = "Port No ")
	port_l.pack(side = BOTTOM)
	
	state = "Enter IP and Port"
	conn_state = Label(conn, text = state)
	connect = Button(conn, text = "Connect")
	quit = Button(conn, text = "Close")
	ip_add = ''
	port_no = ''
	def ip_port():
		global addr
		ip_add = ip.get()
		port_no = port.get()
		
		if (ip_add != '' and port_no != ''):
			addr = (ip_add, port_no)
			print(addr)
			state = "Connecting to " + ip_add + ":" + str(port_no)
			conn_state.config(text=state)
			#connect.config(state=DISABLED)
			c = connection()
			if c == 1:
				state = "Connection Failed, check ip and port!"
				conn_state.config(text=state)
			elif c == 0:
				conn.destroy()
			
		else:
			print("Invalid IP and Port!")
			state = "Invalid IP and Port!"
			conn_state.config(text=state)
	def qt():
		conn.destroy()
		exit()	
	
	quit.pack(side=BOTTOM,pady=10)
	connect.pack(side=BOTTOM)
	connect.config(command=ip_port)
	quit.config(command = qt)
	conn_state.pack(pady=10)
	conn.mainloop()

def connection():
	global c_sock
	#c_sock = socket(AF_INET, SOCK_STREAM)
	try:
		c_sock.connect(addr)
		#print(c_sock)
		print("connected(check)")
		c_sock.send(bytes("server", "utf8"))
		return 0
	except Exception as e:
		print(e)
		return 1


def end_game():
	c_sock.close()

connec()
#send()
sender()
atexit.register(end_game)
