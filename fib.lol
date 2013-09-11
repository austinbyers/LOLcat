HAI
BTW This program prints every fibonacci number in a specified range
BTW Austin Byers, 2013

	U SEEZ "I will find your fib numbers!\nWhere do U want to start?"
	GIMMEH start_num

	U SEEZ "Where do U want to end?"
	GIMMEH end_num

	OBTW fibonacci is our main variable
		 second_fib is the fib number right before fibonacci 
	TLDR
	I HAS A fibonacci ITZ 1 
	I HAS A second_fib ITZ 1

	I HAS A printflag ITZ FAIL   BTW This means False
	I HAS A finishflag ITZ FAIL

	HOW DUZ I get_next_fib ?
		I HAS A tempvar ITZ fibonacci
		LOL fibonacci IZ NOW fibonacci PLUS second_fib
		LOL second_fib IZ NOW tempvar
	IF U SAY SO

	HOW DUZ I set_flags ?
		BTW Check to see if we have finished
		IZ fibonacci BIGR THAN end_num ?
			YARLY
				LOL finishflag IZ NOW WIN
				KTHX
			NOWAI
				IZ fibonacci LIEK end_num ?
					YARLY
						LOL finishflag IZ NOW WIN
						KTHX
				KTHX
		
		BTW Check to see if we are in printing range
		IZ fibonacci SMALLR THAN start_num ?
			NOWAI
				BTW We don't have to have a YARLY block
				IZ fibonacci BIGR THAN end_num ?
					YARLY
						LOL printflag IZ NOW FAIL
						KTHX
					NOWAI
						LOL printflag IZ NOW WIN
						KTHX
			KTHX
	IF U SAY SO

	BTW This is the recursive method
	HOW DUZ I run_program ?
		get_next_fib
		set_flags
		IZ printflag LIEK WIN ?
			YARLY
				U SEEZ fibonacci
				KTHX
		IZ finishflag LIEK WIN ?
			YARLY
				GTFO	BTW This means return
				KTHX
			NOWAI
				run_program
				KTHX
	IF U SAY SO

	run_program	

	BTW This is just to test math operations
	I HAS A magic_number ITZ second_fib MINUS start_num PLUS fibonacci MINUS end_num
	U SEEZ "YR MAGIC NUMBAR IZ:"
	U SEEZ magic_number TIEMZ magic_number DIVIED 2

KTHXBYE

