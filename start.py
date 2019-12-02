from tkinter import *
import os
from threading import Thread

def main():
	master = Tk()
	master.title("Multi Projection")
	master.geometry('200x200')
	server = Button(master, text = "Lunch Server", width = 20)
	server.pack(pady=10)
	sender = Button(master, text = "Lunch Sender", width = 20)
	sender.pack(pady=10)
	project = Button(master, text = "Lunch Projection", width = 20)
	project.pack(pady=10)
	server.config(command = srv)
	sender.config(command = snd)
	project.config(command = pjt)
	close = Button(master, text = "Close", command = master.destroy, width = 20)
	close.pack(pady=10)
	master.mainloop()
	
def srv():
	Thread(target = os.system, args = ("python3 cute_server.py",)).start()

def snd():
	Thread(target = os.system, args = ("python3 naughty_server.py",)).start()
	
def pjt():
	Thread(target = os.system, args = ("python3 little_client.py",)).start()
	
	
main()
