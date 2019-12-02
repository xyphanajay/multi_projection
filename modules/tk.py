from tkinter import *
import os

def tk_m(name):
        size = len(name)
        leng = int(size / 20)
        root = Tk()
        root.title("Message")
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(str(sw) + 'x' + str(sh))
        msg = Message(root, text = name, padx = 20, pady = 20, width = sw - 50)
        msg.config(bg='lightgreen', font=('times', 24, 'bold'))
        msg.pack()
        #lbl.grid(column=2, row=2)
        root.mainloop()

def op():					# used in mailbox()
	f_list.insert(END, "file_name")

def update_ser(user, ty):			# used in ser()
	print(user)
	if ty == "rec":
		rec.insert(END, user)
	elif ty == "sen":
		sender.insert(END, user) 

def rem_client(user, ty):
	print("printing user:")
	print(user)
	try:
		if ty == "rec":
			rec.delete(user)
		elif ty == "sen":
			sender.delete(user)
	except Exception as e:
		print("printing sender:")
		print(sender.get(0,"end"))
		print("printing rec:")
		print(rec.get(0,"end"))
		#print(sender.get(0,"end").index(user))

def ser():					# used as module in cute server				
	serv = Tk()
	serv.title("Connections")
	serv.geometry('230x200')
	
	global sender_l, sender, rec_l, rec
	sender_l = Label(serv, text="Sender List")
	sender_l.pack()
	sender = Listbox(serv, height = 3)
	sender.pack()
	rec_l = Label(serv, text = "Projecter List")
	rec_l.pack()
	rec = Listbox(serv, height = 3)
	rec.pack()
	def qt():
		serv.destroy()
		os._exit(1)	
	close = Button(serv,text="Close Server", command = qt)
	close.pack(pady=10)
	serv.mainloop()
	
	

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
	f_open.config(command=op)
	
	#main.mainloop()

msg = "yo"

def sender():
	
	send = Tk()
	send.title("Sender Portal")
	send.geometry('280x320')
	fr = Frame(send)
	fr.pack()
	
	sbut = Button(fr, text = "Send")
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
		print(p.get())
		#call sender
	sbut.config(command=s_button)
	
	


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
		ip_add = ip.get()
		port_no = port.get()
		print(type(port_no))
		print(type(port))
		if (ip_add != '' and port_no != ''):
			addr = ip_add + ":" + str(port_no)
			print(addr)
			state = "Connecting to " + ip_add + ":" + str(port_no)
			conn_state.config(text=state)
			
			#connect.config(state=DISABLED)
			connect.config(text="Reset", command = reset)
			
		else:
			print("Invalid IP and Port!")
			state = "Invalid IP and Port!"
			conn_state.config(text=state)
			
	def reset():
		ip.set("")
		port.set("")
		state = "Connection Reset: Done"
		conn_state.config(text=state)
		connect.config(text='Connect', command = ip_port)	
	
	quit.pack(side=BOTTOM,pady=10)
	connect.pack(side=BOTTOM)
	connect.config(command=ip_port)
	quit.config(command = conn.destroy)
	conn_state.pack(pady=10)
	
	#return ip_add, port_no
	

