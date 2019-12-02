import subprocess
from modules.tk import tk_m, mailbox
from threading import Thread

def open_file(name, os, types):
	global td				# tk thread for mailbox
	#name = name + "&"
	
	if types == 'text' and name != "file":
		tk_m(name)
	elif types == 'file':
		name = "./files/"+ name
		if os == 'linux':
			#if prior == 0:
			td = Thread(target = linux, args = (name,)).start()
			#elif prior == 1:
			#	subprocess.run(['notify-send', name + " received, check mailbox!"])
				
				
		elif os == 'windows':
			td = Thread(target = windows, args = (name, prior, )).start()
		
def linux(name):
	try:
        	#Thread(target = linux_thread, args = (name,)).start()
		rc = subprocess.run(['xdg-open', name])
		rc = rc.returncode
	except Exception as e:
		print("EXception: Closed file.")

def linux_thread(name):
        subprocess.run(['xdg-open', name])
		
def windows(name):
	try:
		#Thread(target = win_thread, args = (name,)).start()
		rc = subprocess.Popen('powershell.exe start ' + name)
		rc = rc.returncode
	
	except Exception as e:
		print("Exception: Closed file.")

def win_thread(name):
        subprocess.Popen('powershell.exe start ' + name)

