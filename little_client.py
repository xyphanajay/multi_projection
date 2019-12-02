from socket import AF_INET, socket, SOCK_STREAM, SHUT_WR
import modules.file_handle as dealer
import modules.os_detect as detect
import subprocess
import time
import atexit
from pathlib import Path
from threading import Thread
from modules.feature import streak
import sys
from progress.bar import Bar
from tkinter import *




file_pending = 0
prior = 0
file_list = []

buff = 1024
addr = ()
c_sock = socket(AF_INET, SOCK_STREAM)

os = detect.check_os()                       # check os present
txt = "text"
fi = "file"
'''
try:
	host = sys.argv[1]
except Exception as e:
	host = input("server ip: ")
try:
	port = sys.argv[2]
except Exception as e:
	port = input("port no: ")


print("connecting... " + str(addr))
c_sock = socket(AF_INET, SOCK_STREAM)
c_sock.connect(addr)
print("connected(check)")
c_sock.send(bytes("client", "utf8"))
'''
def rec():
	flag = 0
	while True:
		try:
			print("waiting for msg...")
			msg = ""
			time.sleep(1)
			msg = c_sock.recv(buff).decode("utf8")
			if msg:
				print("Display ~> " + msg)
				#subprocess.run(["notify-send", msg])
				#display(msg)
				dealer.open_file(msg, os, txt)
			elif msg == '':
				raise RuntimeError("socket conn broken")
				c_sock.close()
				break
				
			if msg == "quit" and flag == 0:
				print("breaking out")
				c_sock.shutdown(SHUT_WR)
				#c_sock.close()
				#break
			if msg == "file":
				file_recv()
				
					
		except OSError:
			print("error")
			c_sock.shutdown(SHUT_WR)
			c_sock.close()
			break

def mailbox():
	global main, f_open, f_list, scroll, fr
	main = Tk()
	main.title("Mailbox")
	main.geometry('300x180')
	
	head = Label(main, text = "Pending Files")
	head.pack(side = TOP, padx = 20, pady = 15)
	fr = Frame(main)
	fr.pack()
	
	f_list = Listbox(fr, height = 4)
	scroll = Scrollbar(fr, orient = VERTICAL)
	f_list.pack(side=LEFT)
	scroll.pack(side=RIGHT, fill=Y)
	scroll.config(command=f_list.yview)
	f_list.config(yscrollcommand=scroll.set)
	
	f_open = Button(main, text = "Open")
	f_open.pack(side=BOTTOM, padx=20)
	f_open.config(command=mb_open)
	
	main.mainloop()

def update_mb(name):					# used in mailbox()
	f_list.insert(END, name)

def mb_open():
	global file_list
	loc = f_list.curselection()
	name = file_list[loc[0]]
	f_list.delete(loc)
	dealer.open_file(name, os, fi)
			
def file_recv():
	try:
		global file_list
		raw = c_sock.recv(buff).decode("utf8")
		info = raw.split("#")
		name = info[1]
		size = int(info[2])
		prior = int(info[3])
		i_key = int(info[4]) 
		streak()
		print("File Info:")
		print("Name: " + name + "\tSize: " + str(size))
		print("Priority: "+ str(prior) + "\tKey: " + str(i_key))
		if name == "fail":
		#	dump = c_sock.recv(buff)
		#	print("Dumpping")
		#	print(dump)
			print("Error: File not received! Contact Adminstrator.")
			dealer.open_file("File not received!", os, txt)
			streak("=")
			return 0
		name = file_check(name)
		f = open("./files/"+name, 'wb')
		with Bar('Downloading', max = size) as bar:
			while size:
				size -= 1 
				data = ""
				data = c_sock.recv(buff)
				if not data:
					break
				f.write(data)
				bar.next()
		f.close()
		
		# XOR implementation
		fo = open("./files/"+name, 'rb')
		image = fo.read()
		fo.close()

		image = bytearray(image)

		for index, value in enumerate(image):
			image[index] = value^i_key
	
		fo = open("./final/" + name, 'wb')
		fo.write(image)
		fo.close()
	
		if prior == 0:
			dealer.open_file(name, os, fi)
		elif prior == 1:
			file_list.append(name)
			update_mb(name)
			subprocess.run(['notify-send', name+" received, open via mailbox!"])
	except Exception as e:
		print("LOG: File not received!")
		print(e)
		dealer.open_file(raw, os, txt)
		return


def file_check(name, i = 1):
	my_file = Path("./files/" + name)
	if my_file.is_file():
		name = file_check(ren(name))
	return name

def ren(name):
	rn = ""
	part = name.split(".")
	extn = part[len(part) - 1]
	for p in part:
		if p != extn:
			rn += p
	rn = rn + "x." + extn
	return rn

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
		c_sock.send(bytes("client", "utf8"))
		return 0
	except Exception as e:
		print(e)
		return 1


def end_game():
	c_sock.close()

connec()
Thread(target = mailbox).start()
rec()
atexit.register(end_game)
