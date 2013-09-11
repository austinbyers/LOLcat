#!/usr/bin/python
# This python code was compiled from LolCode with lolcat
# Credit: Austin Byers, 2013
# LOL source file: /home/austin/Dropbox/Ubuntu/final/source.lol

# This program prints every fibonacci number in a specified range 
# Austin Byers, 2013 

print "I will find your fib numbers!\nWhere do U want to start?" 
start_num = float(raw_input("GIMMEH YR start_num: ")) 

print "Where do U want to end?" 
end_num = float(raw_input("GIMMEH YR end_num: ")) 

""" fibonacci is our main variable 
second_fib is the fib number right before fibonacci 
""" 
fibonacci = 1 
second_fib = 1 

printflag = False # This means False 
finishflag = False 

def get_next_fib(): 
	global finishflag
	global second_fib
	global end_num
	global fibonacci
	global start_num
	global printflag
	
	tempvar = fibonacci 
	fibonacci = fibonacci + second_fib 
	second_fib = tempvar 
	return 

def set_flags(): 
	global finishflag
	global second_fib
	global end_num
	global fibonacci
	global start_num
	global printflag
	
	# Check to see if we have finished 
	if ( fibonacci > end_num ): 
		
		finishflag = True 
		pass 
	else: 
		if ( fibonacci == end_num ): 
			
			finishflag = True 
			pass 
		pass 
	
	# Check to see if we are in printing range 
	if ( fibonacci < start_num ): 
		pass 
	else: 
		# We don't have to have a YARLY block 
		if ( fibonacci > end_num ): 
			
			printflag = False 
			pass 
		else: 
			printflag = True 
			pass 
		pass 
	return 

# This is the recursive method 
def run_program(): 
	global finishflag
	global second_fib
	global end_num
	global fibonacci
	global start_num
	global printflag
	
	get_next_fib() 
	set_flags() 
	if ( printflag == True ): 
		
		print fibonacci 
		pass 
	if ( finishflag == True ): 
		
		return # This means return 
		pass 
	else: 
		run_program() 
		pass 
	return 

run_program() 

# This is just to test math operations 
magic_number = second_fib - start_num + fibonacci - end_num 
print "YR MAGIC NUMBAR IZ:" 
print magic_number * magic_number / 2 




