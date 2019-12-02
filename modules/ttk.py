from tkinter import *
from time import sleep





def b():
	print(str(v.get()))
	lb.insert(END,str(v.get()))
	
def bb():
	print(str(lb.curselection()))

def bbb():
	x = []
	x.append("work")
	x.append("working")
	x.append("oops")
	print(x)
	for y in x:
		lb.insert(END, str(y))

def work():
	global main, b1, b2, v, e, lb, sb, b3
	main = Tk()
	b1 = Button(main, text="Button")
	b2 = Button(main, text = "Drag")
	b3 = Button(main, text="list up")
	b3.pack(side=RIGHT, padx=10)
	v = StringVar()
	e = Entry(main,textvariable=v)
	lb = Listbox(main, height=3)
	sb = Scrollbar(main, orient=VERTICAL)
	b2.pack(side=LEFT, padx=10)
	b1.pack(side=RIGHT, padx=20)
	b1.configure(text="Drop")
	e.pack()
	print("printing var v:")
	print(str(v.get()))
	v.set("fuck it")
	lb.pack(side=BOTTOM)
	lb.insert(END, "die mf")
	lb.insert(END, "hell sob")
	sb.pack(side=RIGHT, fill=Y)
	sb.config(command=lb.yview)
	lb.config(yscrollcommand=sb.set)
	print(str(lb.curselection()))
	b1.config(command=b)
	b2.config(command=bb)
	b3.config(command=bbb)
	main.mainloop()
	



