import subprocess
from tkinter import *
from threading import Thread

def open_file(name, os, types):
	if os == 'linux':
		#linux(name, types)
		Thread(target = linux, args = (name, types,)).start()
		
	elif os == 'windows':
		#windows(name, types)
		Thread(target = windows, args = (name, types,)).start()
		
def linux(name, types):
	if types == 'text':
		tk_m(name)
	
	elif types == 'file':
                #Thread(target = linux_thread, args = (name,)).start()
		subprocess.run(['xdg-open', name])

def linux_thread(name):
        subprocess.run(['xdg-open', name])
		
def windows(name, types):
	if types == 'text':
                tk_m(name)
                """f = open('notifi.ps1', 'w')
		d = "New-BurntToafkastNotification -Text "
		f.write(d + "\"" + name + "\"" + ", " + "\'" + name + "\'")
		f.close()"""
	
	elif types == 'file':
                #Thread(target = win_thread, args = (name,)).start()
		subprocess.Popen('powershell.exe start ' + name)

def win_thread(name):
        subprocess.Popen('powershell.exe start ' + name)
		
def tk_l(name):
	window = Tk()
	window.title("Message")
	sw = window.winfo_screenwidth()
	sh = window.winfo_screenheight()
	window.geometry(str(sw) + 'x' + str(sh))
	lbl = Label(window, text = name, font=("Helvetica", 20))
	lbl.grid(column=2, row=2)
	#lbl.place(x=sh, y=sw, anchor="center")
	window.mainloop()

def tk_m(name):
        size = len(name)
        leng = int(size / 20)
        root = Tk()
        root.title("test2")
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(str(sw) + 'x' + str(sh))
        msg = Message(root, text = name, padx = 20, pady = 20, width = sw - 50)
        msg.config(bg='lightgreen', font=('times', 24, 'bold'))
        msg.pack()
        #lbl.grid(column=2, row=2)
        root.mainloop()

