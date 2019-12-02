
def cfile(name):				#check file exists or not
	if name.is_file():
		return 0			# file exists return 0
	else:			
		return 1			# file not found return 1
		
		
def streak(symb = ""):
	if symb == "":
		print("#"*30)
	else:
		print(symb*30)
