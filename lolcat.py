#!/usr/bin/python
# lolcat - LOL Compile And Test
# (c) Austin Byers, 2013
# See the printed help below for more information

import re
import os
import sys

# ========== Check Arguments ==========
try:
	source_path = sys.argv[1]
except IndexError, e:
	print >> sys.stderr, "lolcat: I CAN HAS MORE ARGS? IF U WANT TO RUN YR CODE, TRY: lolcat [LOL Source File] "
	print >> sys.stderr, "OR, IF U WANT TO SEEZ MAI PYHTON FIEL, TRY: lolcat [LOL Source File] [Python Destination File]"
	print >> sys.stderr, "OR, IF U R DUMBER TAHN UR CAT, TRY: lolcat --help"
	raise SystemExit(2)

# ========== Print Help ===========

if (source_path.lower() == "--help"):
	print "lolcat: The LOLCODE Python Translator. (c) Austin Byers, 2013"
	print "Please Note: This implementation of LOLCODE is slightly different than the original"
	print "(and henceforth, 'LOLCODE' refers to THIS implementation). Visit LOLCODE.com for the 'official' documentation."
	
	print "\nUsage: lolcat --help | lolcat [Source File] | lolcat [Source File] [Destination File]"
	print "For example: $ ./lolcat source.lol translation.py"
	
	print "\n--------------------------- OHAI! -------------------------- "
	print "\nThe lolcat parser translates each line of the LOLCODE into Python code, which it stores as a string in memory."
	print "All whitespace, except newlines and space between words, is ignored."
	print "If only the source file is specified, the parser will execute the code contained therein and quit."
	print "Otherwise, the parser will NOT execute the program, but will write the translated python file to the specfied destination."
	
	print "\nThe goal of writing this program was to be able to catch all syntax errors BEFORE running/writing the translated python code."
	print "This is accomplished with a finite state automata. Every token that is read causes the parser to go to a different state,"
	print "and there are only a finite number of possible states that can be reached from any point in the parsing."
	
	print "\nLOLCODE is Turing complete, although it's a bit cumbersome to use. (This entire project was completed in 3 days for"
	print "a computer science final, so I only had to time to implement the very basics of the language!) Most notably,"
	print "there are no functions, only methods, because return values aren't supported. Instead, global variables can be used"
	print "to communicate across methods. (True programmers should be twitching violently after reading that last sentence!)"
	print "There also aren't any loops (that's what recursion is for!)"

	print "\nThe Parser class that is implemented was designed to enable some degree of universality. After all, every parser"
	print "has to check for unfinished statements and keep track of variable types, function names, comments, etc."
	print "The Parser class is the heart of the program, and this organization makes it relatively straightforward to add support"
	print "for more keywords and improve the functionality of the language, if anyone ever wanted to take lolcat to the next level."

	print "\n------------------- KEWYWORD SUMMARY -------------------"
	print "HAI / KTHXBYE"
	print "HOW DUZ I method_name ? / GTFO / IF U SAY SO"
	print "IZ value OP value ?"
	print "BIGR THAN, SMALLR THAN, or LIEK"
	print "YARLY / NOWAI / KTHX"
	print "WIN / FAIL"
	print "PLUS / MINUS / TIEMZ / DIVIED"
	print "I HAS A variable ITZ value"
	print "LOL variable IZ NOW new_value"
	print "BTW or OBTW/TLDR"

	print "\n------------------- CONTROL FLOW -------------------"
	print "All LOLCODE programs must begin with 'HAI' and end with 'KTHXBYE' This is very important -"
	print "if you do not properly greet the lolcat, he will hiss and spit hairballs at you. While shredding all of your toilet paper. o_O"
	print "\nMethods are defined with 'HOW DUZ I method_name ?' Lolcat is an inquistive creature,"
	print "and all questions  must actually end in a question mark (separated by a space). Methods are closed with 'IF U SAY SO'"
	print "Methods cannot return values (though this could be easily implemented in future versions), but they can modify"
	print "global variables or variables within their own scope. And you can always 'GTFO' of a method early, you pansy."
	print "\n'If' statements look like: 'IZ value OP value ?' where 'value' can be any TROOF, YARN, NUMBAR, math expression"
	print "involving NUMBARS, or previously defined variable. 'OP' can be 'BIGR THAN' (>), 'SMALLR THAN' (<), or 'LIEK' (==)"
	print "The if statement must be followed by a 'YARLY' and/or a 'NOWAI' (i.e. else) block. These blocks must be closed with "
	print "'KTHX', although they may otherwise be empty."

	print "\n------------------- TYPES and VARIABLES -------------------"
	print "There are three types: TROOF (bool), which can have the value of 'WIN' or 'FAIL'; YARN (string); NUMBAR (int/float)"
	print "and a VAR (which just represents one of these types). Types are not declared - they are inferred by the purrser."
	print "The types cannot explicitly be changed, but a reassignment of a variable will also reassign that variable's type."
	print "A variable is cheerfully declared by 'I HAS A varname ITZ value' where 'value' can be of any type or numeric expression."
	print "A variable is reassigned with 'LOL varname IZ NOW newvalue' These actually translate to the same Python statement, but the"
	print "difference is stressed both for readibility of the LOLCODE and for the user's safety - if the user tries to re-assign"
	print "a variable that is outside of the current function, Python creates a local copy, and the change will NOT carry over."
	print "But lolcat is nicer than python, and he will kindly inform the programmer of their stupidity."
	print "\nMath expressions take the form 'value OPERATOR value OPERATOR value...' and support the operators"
	print "PLUS, MINUS, TIEMZ, and DIVIED. Of course, lolcat will complain if the user tries to add non-numeric types." 

	print "\n------------------- INPUT and OUTPUT -------------------"
	print "Printing to stdout is done with 'U SEEZ value'. (Currently, string operations are not supported)"
	print "Getting input from the user looks like 'GIMMEH varname.' LOLCODE specifies input to be a 'float' by default."
	
	print "\n------------------- COMMENTS -------------------"
	print "'BTW' causes the rest of the current line to be ignored by the compiler. OBTW and TLDR, respectively, specify"
	print "the start and end of a multi-line commment block. Anything in a comment is directly copied to the (optional) output file."
	
	print "\n------------------- PARSER ERRORS -------------------"
	print "There are basically three kinds of errors:"
	print "WTF errors are thrown when the parser encounters an unrecognized token. This means you don't know what the hell you're doing."
	print "OMG errors are thrown when the parser encounters an unexpected End of Line. This means you should go home and come back tomorrow."
	print "ROTFLOL errors are thrown when the parser encounters an unexpected End of File. This means you are a humiliating failure."

	print "\n------------------- KTHXBYE! -----------------------"
	print "OMG, If u read this far, u need a life. LOL "
	print "\n  :) Austin (:\n"

	raise SystemExit(2)

# ========== Error Handling ==========

def print_error(msg, parser, error_type):
	# Uncomment for debugging:
	# print parser.stack, parser.states

	print >> sys.stderr, "lolcat: O NOES! U HAS ERROR :("
	print >> sys.stderr, "    line " + str(parser.lineno) + ": " + parser.line.strip()
	if (error_type == "token-error"):
		# Unrecognized Token Error - print the last word parsed
		print >> sys.stderr, "    " + "WTF IS '" + parser.word + "'? "
	elif (error_type == "EOL-error"):
		print >> sys.stderr, "    OMG! I WAZNT EXPCTING YR LINE TO END!"
	elif (error_type == "EOF-error"):
		print >> sys.stderr, "    ROTFLOL! I WAZNT EXPCTING YR FILE TO END!"
	if (msg != ""):
		print >> sys.stderr, "    " + msg
	raise SystemExit(1)

# ========== Parser Class ========== 

class Parser(object):

	def __init__(self):
		# We keep a list of parser states in order of depth
		# Thus, states[-1] represents the most recent state encountered
		self.states = ["initial"]

		# The stack keeps track of all of the functions currently within the parser's scope
		# Each function-tuple has name, depth, and variable dictionary
		self.stack = [("__GLOBAL__", 0, {})]

		# The visible scope includes all functions at or "above" our current depth
		# I.e. a function is visible if its depth <= self.depth
		# This also indicates how many tabs to put before the current line
		self.depth = 0

		# As the code is compiled, it is stored as a string in memory
		header = "#!/usr/bin/python\n# This python code was compiled from LolCode with lolcat\n" + \
		"# Credit: Austin Byers, 2013\n# LOL source file: " + os.path.abspath(source_path) + "\n"
		self.code = header
		self.lineno = 1

		# Temporary storage - erased after each line read
		self.line = ""
		self.word = ""
		self.curvar = ""	

	# These are broken off as their own functions for debugging purposees
	# (You can print the state of the parser before changing it, for example)
	def new_state(self, state): self.states.append(state)
	def pop_state(self): self.states.pop()

	# ~~~~~~~~~~ String Validation ~~~~~~~~~~~

	# check for un-escaped quote marks in a string
	def check_quotes(self, word, start, end):
		if (re.search(r'[^\\]\"', word[start:end]) != None):
			# Un-escaped quote mark between start and end:
			print_error("IF U WANT QUOTS IN A YARN, DO LIKE DIS: \"1,2,3 \\\" quote for me\"", self, "token-error")

	# check for name clashes and special characters
	def check_name(self, word):
		lol_keywords = ["HAI", "KTHXBYE", "U", "SEEZ", "I", "HAS", "A", "ITZ", "WIN", "FAIL", "GIMMEH", "HOW", "DUZ", "I", "IF", 
			"SAY", "SO", "IZ", "BIGR", "THAN", "LIEK", "SMALLR", "PLUS", "TIMEZ", "MINUS", "DIVIED", "YARLY", "NOWAI", "KTHX"]
		python_keywords = ["and", "as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "except", "exec", "finally", "for", 				"from", "global", "if", "import", "in", "is", "lambda", "none", "not", "or", "pass", "print", "raise", "return", "try", "while", 				"with", "yield"]
		if word in lol_keywords or word in python_keywords:
			print_error("UR VAR MUZT NOT BE SAEM AS MY KEYWURDS", self, "token-error")
		elif (not word[0].isalpha()):
			print_error("THE FURST LETTER IN UR VAR NAME MUZT BE A LETTER", self, "token-error")
		else:
			for char in word:
				if (not char.isalnum() and not char == "_"):
					print_error("UR VAR NAME MUZT HAS ONLY LETTERS AN NUMBRS AN UNDERSCOAR", self, "token-error")

	# A word is numeric if it is a VAR with type NUMBAR or it is all digits except
	# at most 1 decimal point and a leading negative sign are allowed
	# (Python is actually much more flexible with numbers, but we limit them here for simplicity)
	def is_numeric(self, word):
		if (self.get_var_type(word) == "NUMBAR"): return True
		if (word.count('.') <= 1 and word.replace('.','').replace('-','').isdigit()):
			if word[0].isdigit() and word.count('-') == 0: return True
			elif word[0] == "-" and word.count('-') == 1: return True
		# if it doesnt satisfy the above conditions, return False
		return False

	# ~~~~~~~~~~ Stack Searching ~~~~~~~~~~
	# Search for matches in REVERSE stack order. I.e. Look for matches in our current block, then our parents, etc.

	# return the type of the given variable (or "NONE" if variable not found)
	def get_var_type(self, varname):
		for function, depth, varlist in self.stack[::-1]:
			if varname in varlist and depth <= self.depth:
				return varlist[varname]
		return "NONE"

	# In Python, variable declaration always creates a local copy unless a variable already exists
	# AT THE CURRENT DEPTH. Thus, this method is called when we are re-assigning a variable with LOL var IZ NOW...
	# because we can't reassign the value of a variable unless it is global or at our same depth
	def get_limited_var_type(self, varname):
		for function, depth, varlist in self.stack:
			if varname in varlist and (depth == 0 or depth == self.depth):
				return varlist[varname]
		return "NONE"
			
	# check whether a function name is in our current scope
	# (In the future, this may return function type)
	def is_function(self, fname):
		for function, depth, varlist in self.stack[::-1]:
			if (fname == function) and (depth <= self.depth + 1):
				# Function names live at the same depth as the functions themselves. For example, 
				# if we are at depth 0 (global scope), any function declarations will be marked as depth 1
				return True
		return False

	# Any nested functions are now out of our visible scope and can be removed from the stack
	# This should be called whenever depth is decreased (i.e. after if-blocks and function-blocks)
	def lower_depth(self):
		while (self.stack[-1][1] > self.depth):
				self.stack.pop()
		self.depth -= 1

	# In python, global variables cannot be changed from within a function unless they have
	# been explicitly declared as global. This is not what we want, so this method appends 
	# global variable declarations for global variables - this should be called for every new function
	def add_global_vars(self):
		for var in self.stack[0][2]:
			self.code += "global " + var + "\n"
			self.begin_line(self.line)

	# Set the type of a variable. This searches for the first function on the stack that is the 
	# same depth as the parser
	def set_var_type(self, var, vartype):
		for function, depth, varlist in self.stack[::-1]:
			if (depth == self.depth):
				varlist[var] = vartype

	# ~~~~~~~~~~~ Parsing Functions ~~~~~~~~~~~

	def begin_line(self, line):
		# Add the correct amount of tabs before the next line
		tabs = self.depth
		while (tabs != 0):
			self.code += "\t"
			tabs -= 1		
		self.line = line

	# The parser is set up as a Finite State Machine (Automata). A massive 'if/elif' block determines
	# what action to take based on the parser's current state and the next word.
	def read_word(self, word):
		self.word = word

		if (word == ""):  pass	#ignore blank words (spaces are added automatically by the parser)

		# ---------- Main States ----------

		elif (self.states[-1] == "initial"):
			if (word == "HAI"):
				self.new_state("hai")
			else:
				print_error("PLZ SAY 'HAI' AT START OF PROGRM! KTHX", self, "token-error")

		elif (self.states[-1] == "hai" or self.states[-1] == "function" or self.states[-1] == "YARLY" or self.states[-1] == "NOWAI"):
			if (word == "BTW"):
				self.append_code('#')
				self.new_state("single-line-comment")
			elif (word == "OBTW"):
				self.append_code('\"\"\"')
				self.new_state("multi-line-comment")
			elif (word == "U"):			self.new_state("U...")
			elif (word == "I"):			self.new_state("I...")
			elif (word == "GIMMEH"):	self.new_state("GIMMEH...")
			elif (word == "HOW"):		self.new_state("HOW...")
			elif (word == "LOL"):		self.new_state("LOL...")
			elif (self.is_function(word)):
					self.append_code(word + "()")
					self.new_state("EOL")
			elif (word == "IZ"):
				self.append_code("if (")
				self.new_state("IZ...")
	
			# Block termination keywords
			elif (word == "GTFO"):
				if "function" in self.states:
					self.append_code("return")
				else:
					print_error("YR NOT IN A FUNCTN AN U CANT GTFO!", self, "token-error")
			elif (word == "KTHX"):
				self.append_code("pass") # for safety, this is added at the end of if statements (in case they are empty)
				self.lower_depth()
				if (self.states[-1] == "YARLY"):
					self.pop_state()
					self.new_state("yes-if-block")
					self.new_state("EOL")
				elif (self.states[-1] == "NOWAI"):
					self.pop_state()
					self.new_state("EOL")
				else:
					print_error("KTHX FR WUT? I DONT SEEZ YR FUNCTN!", self, "token-error")
			elif (word == "IF"):
				if (self.states[-1] == "YARLY" or self.states[-1] == "NOWAI"):
					print_error("PLZ END 'IZ... ?' WITH 'KTHX' BEFORE U SAYZ 'IF (U SAY SO)'", self, "token-error")
				elif (self.states[-1] == "hai"):
					print_error("TRY 'IZ var BIGR THAN 20 ?' TO MAEK COMPAIRSON", self, "token-error")
				else:
					self.new_state("IF...")
			elif (word == "KTHXBYE"):
				if (self.states[-1] == "YARLY" or self.states[-1] == "NOWAI"):
					print_error("PLZ END 'IZ... ?' WITH 'KTHX' BEFORE U SAYZ 'KTHXBYE'", self, "EOF-error")
				elif (self.states[-1] == "function"):
					print_error("PLZ END YR FUNCTN BEFORE U SAYZ 'KTHXBYE;", self, "EOF-error")
				else:
					# valid program end
					self.pop_state()
					self.new_state("end")
	
			else: print_error("", self, "token-error")

		# No more input expected on the current line (except comments)
		elif (self.states[-1] == "EOL"):
			if (word == "BTW"):
				self.append_code('#')
				self.pop_state()
				self.new_state("single-line-comment")
			elif (word == "OBTW"):
				# python doesn't allow multi-line comments after code
				print_error("SRY, PYTHON DOZNT LIEK THIS HERE. USE 'BTW' INSTEAD", self, "token-error")
			else:
				print_error("PLZ DONT PUT THIS HERE. KTHX", self, "token-error")

		elif (self.states[-1] == "end"):
			print_error("PLZ DONT PUT TXT AFTR U SAY 'KTHXBYE'", self, "token-error")

		# ---------- Value States ----------

		# We have a number, which could be followed by an operator
		elif (self.states[-1] == "number..."):
			self.pop_state()
			if (word == 'PLUS'):
				self.append_code('+')
				self.new_state("number op...")
			elif (word == "MINUS"):
				self.append_code('-')
				self.new_state("number op...")
			elif (word == "TIEMZ"):
				self.append_code('*')
				self.new_state("number op...")
			elif (word == "DIVIED"):
				self.append_code('/')
				self.new_state("number op...")
			else:  
				# next token is not an operator, read the current word in its former context
				self.read_word(word)

		# we have an operator, and are expecting another number...
		elif (self.states[-1] == "number op..."):
			if self.is_numeric(word):
				self.append_code(word)
				self.pop_state()
				self.new_state("number...")
			else:
				print_error("ITZ NOT A NUMBAR! PLZ GIMMEH NUMBAR... KTHX", self, "token-error")

		elif (self.states[-1] == "string"):
			self.check_quotes(word, 0, -1) # The only allowed unescaped quote mark is at the end of the word
			self.append_code(word)
			if (word[-1] == '"' and word != "\\\""):
				# IF the word ends with a quote mark and isn't \", the string is over
				self.pop_state()

		# ---------- Conditional States ----------
		
		# handle all of these states together:
		elif (self.states[-1] == "IZ..." or self.states[-1] == "IZ var op THAN..." or self.states[-1] == "IZ var LIEK..."):
			if (self.states[-1] == "IZ..."): 
				# first half of if statement
				self.pop_state()
				self.append_value(word, "IZ var...")
			else:
				# second half of if statement
				self.pop_state()
				self.append_value(word, "IZ var op value...")

		elif (self.states[-1] == "IZ var..."):
			if (word == "BIGR"):
				self.append_code('>')
				self.pop_state()
				self.new_state("IZ var op...")
			elif (word == "SMALLR"):
				self.append_code('<')
				self.pop_state()
				self.new_state("IZ var op...")
			elif (word == "LIEK"):
				self.append_code('==')
				self.pop_state()
				self.new_state("IZ var LIEK...")
			else:
				print_error("WHERE IZ YR COMPAIRSON? TRY 'IZ myvar BIGR THAN 50 ?'", self, "token-error")

		elif (self.states[-1] == "IZ var op..."):
			if (word == "THAN"):
				self.pop_state()
				self.new_state("IZ var op THAN...")
			else:
				print_error("WHERE IZ YR COMPAIRSON? TRY 'IZ myvar BIGR THAN 50 ?'", self, "token-error")
		
		# Finish if statement
		elif (self.states[-1] == "IZ var op value..."):
			if (word == "?"):
				self.append_code("):")
				self.depth += 1
				self.pop_state()
				self.new_state("IZ var op value ?")
				self.new_state("EOL")
			else:
				print_error("WHERE IZ YR QSTN MARK? TRY 'IZ myvar BIGR THAN 50 ?'", self, "token-error")

		# next line after if statement
		elif (self.states[-1] == "IZ var op value ?"):
			if (word == "BTW"):
				self.append_code('#')
				self.new_state("single-line-comment")
			elif (word == "OBTW"):
				self.append_code('\"\"\"')
				self.new_state("multi-line-comment")
			elif (word == "YARLY"):
				self.pop_state()
				self.new_state("YARLY")
				self.new_state("EOL")
			elif (word == "NOWAI"):
				# Emtpy YARLY block - add pass statement
				self.append_code("pass")
				self.lower_depth()
				self.code += "\n"
				self.begin_line(self.line)
				self.append_code("else:")
				self.depth += 1
				self.pop_state()
				self.new_state("NOWAI")
				self.new_state("EOL")
			else:
				print_error("USE 'YARLY' AN/OR 'NOWAI' AFTER YR QUESTUN", self, "token-error")

		elif (self.states[-1] == "yes-if-block"):
			# They have finished their if statement - the else block is optional
			if (word == "NOWAI"):
				self.append_code("else:")
				self.depth += 1
				self.pop_state()
				self.new_state("NOWAI")
				self.new_state("EOL")
			else:
				# if no else block, read the next word in its parent context
				self.pop_state()
				self.read_word(word)

		# ---------- Comment States ----------
	
		elif (self.states[-1] == "single-line-comment"):
			self.append_code(word)
	
		elif (self.states[-1] == "multi-line-comment"):
			if (word == "TLDR"):
				self.append_code('\"\"\"')
				self.pop_state()
			else:
				self.append_code(word)

		# ---------- IO States ----------
	
		elif (self.states[-1] == "GIMMEH..."):
			self.check_name(word)
			input_code = word + " = float(raw_input(\"GIMMEH YR " + word + ": \"))"
			self.append_code(input_code)
			# add new variable to current function
			self.set_var_type(word, "NUMBAR") # LOLCODE specifies input to be numeric by default
			self.pop_state()
			self.new_state("EOL")

		elif (self.states[-1] == "U..."):
			if (word == "SEEZ"):
				self.append_code("print")
				self.pop_state()
				self.new_state("U SEEZ...")
			else:
				print_error("TRY 'U SEEZ' \"HAI\"", self, "token-error")

		elif (self.states[-1] == "U SEEZ..."):
			self.pop_state()
			self.append_value(word, "EOL")

		# ---------- Function States ----------

		elif (self.states[-1] == "HOW..."):
			if (word == "DUZ"):
				self.pop_state()
				self.new_state("HOW DUZ...")
			else:
				print_error("TRY 'HOW DUZ I do_something ?'", self, "token-error")
	
		elif (self.states[-1] == "HOW DUZ..."):
			if (word == "I"):
				self.pop_state()
				self.new_state("HOW DUZ I...")
			else:
				print_error("TRY 'HOW DUZ I do_something ?'", self, "token-error")	
	
		# Found new function
		elif (self.states[-1] == "HOW DUZ I..."):
			self.check_name(word)
			self.append_code("def " + word + "():")
			self.pop_state()
			self.new_state("HOW DUZ I function...")

			self.depth += 1
			self.stack.append((word, self.depth, {}))		# Add the function to the runtime stack

		# Found question mark - Finish setting up new function
		elif (self.states[-1] == "HOW DUZ I function..."):
			if (word == '?'):
				self.pop_state()
				self.new_state("function")
				# Append newline, necessary tabs, and global variables
				self.code += "\n"
				self.begin_line(self.line)
				self.add_global_vars()
			else:
				print_error("WHERE IZ YR QSTN MARK? TRY 'HOW DUZ I do_something ?'", self, "token-error")

		elif (self.states[-1] == "IF..."):
			if (word == "U"):
				self.pop_state()
				self.new_state("IF U...")
			else:
				print_error("TRY 'IF U SAY SO' TO END 'HOW DUZ I'", self, "token-error")
	
		elif (self.states[-1] == "IF U..."):
			if (word == "SAY"):
				self.pop_state()
				self.new_state("IF U SAY...")
			else:
				print_error("TRY 'IF U SAY SO' TO END 'HOW DUZ I'", self, "token-error")

		# Found function end
		elif (self.states[-1] == "IF U SAY..."):
			if (word == "SO"):
				self.append_code("return")
				self.pop_state()		# pop the IF U SAY... state
				self.pop_state()		# pop the overlying function state
				self.lower_depth()
				self.new_state("EOL")
			else:
				print_error("TRY 'IF U SAY SO' TO END 'HOW DUZ I'", self, "token-error")

		# ---------- Variable States ----------

		elif (self.states[-1] == "I..."):
			if (word == "HAS"):
				self.pop_state()
				self.new_state("I HAS...")
			else:
				print_error("TRY 'I HAS A number' OR 'I HAS A number ITZ 10'", self, "token-error") 

		elif (self.states[-1] == "I HAS..."):
			if (word == "A"):
				self.pop_state()
				self.new_state("I HAS A...")
			else:
				print_error("TRY 'I HAS A number' OR 'I HAS A number ITZ 10'", self, "token-error")

		# Found new variable
		elif(self.states[-1] == "I HAS A..."):
			self.check_name(word)
			self.append_code(word)
			self.curvar = word
			self.set_var_type(word, "NOOB")
			self.pop_state()
			self.new_state("I HAS A var...")
	
		elif(self.states[-1] == "I HAS A var..."):
			if (word == "ITZ"):
				self.append_code("=")
				self.pop_state()
				self.new_state("I HAS A var ITZ...")
			else:
				print_error("TRY 'I HAS A number' OR 'I HAS A number ITZ 10'", self, "token-error")
	
		# set the value of a variable
		elif(self.states[-1] == "I HAS A var ITZ..."):
			self.pop_state()
			self.set_var_type(self.curvar, self.append_value(word, "EOL"))

		elif(self.states[-1] == "LOL..."):
			self.curvar = word
			if (self.get_limited_var_type(word) == "NONE"):
				print_error("I DONT SEEZ YR VAR! TRY 'I HAS A var' TO MAKE A NEW VAR\n\
    BTW, U CAN ONLY CHANGE GLOBAL VARS OR VARS IN YR CURRENT FUNCTN", self, "token-error")
			self.append_code(word)
			self.pop_state()	
			self.new_state("LOL var...")
	
		elif(self.states[-1] == "LOL var..."):
			if (word == "IZ"):
				self.pop_state()
				self.new_state("LOL var IZ...")
			else:
				print_error("TRY 'LOL myvar IZ NOW 10'", self, "token-error")
			
		elif(self.states[-1] == "LOL var IZ..."):
			if (word == "NOW"):
				self.append_code('=')
				self.pop_state()
				self.new_state("LOL var IZ NOW...")
			else:
				print_error("TRY 'LOL myvar IZ NOW 10'", self, "token-error")

		elif(self.states[-1] == "LOL var IZ NOW..."):
			self.pop_state()
			self.set_var_type(self.curvar, self.append_value(word, "EOL"))

		else:
			print_error("Internal error: state " + self.states[-1] + " not recognized", self, "token-error")

	# Adds a space after the word before adding it to the code
	def append_code(self, word):
		self.code += word + " "

	# Expects the next word to be a "value" - a YARN, NUMBAR, TROOF, VAR, or math expression with NUMBARs
	# Appends the value to the code, returns its type, and sets the next state for the parser
	def append_value(self, word, nextstate):
		self.new_state(nextstate)
		if (word == "WIN"):
			self.append_code("True")
			return "TROOF"
		elif (word == "FAIL"):
			self.append_code("False")
			return "TROOF"
		elif (self.is_numeric(word)):
			self.append_code(word)
			self.new_state("number...")
			return "NUMBAR"
		elif (self.get_var_type(word) != "NONE"):
			self.append_code(word)
			return self.get_var_type(word)
		elif (word[0] == '"'):
			self.check_quotes(word, 1, -1)
			self.append_code(word)
			if (word[-1] != '"'):	
				# multi word string
				self.new_state("string")
			return "YARN"
		else:
			print_error("U NEED A TROOF, NUMBAR, YARN, or VAR. TRY 'IZ myvar BIGR THAN 50 ?'", self, "token-error")

	# Finish parsing the current line - check that our state is valid
	def finish_line(self):
		# Check for states that we should NOT be in:
		if (self.states[-1] == "U..." or self.states[-1] == "U SEEZ..."):
			# Unfinished print statement
			print self.states[-1]
			print_error("WUT DO U SEEZ? TRY 'U SEEZ \"HAI\"'", self, "EOL-error")
		elif(self.states[-1] == "I..." or self.states[-1] == "I HAS..." or self.states[-1] == "I HAS A..."):
			# only partial variable declaration
			print_error("TRY 'I HAS A number' OR 'I HAS A number ITZ 10'", self, "EOL-error")
		elif(self.states[-1] == "I HAS A var ITZ..."):
			# Unfinished variable assignment	
			print_error("TRY 'I HAS A number' OR 'I HAS A number ITZ 10'", self, "EOL-error")
		elif(self.states[-1] == "GIMMEH..."):
			# Unfinished input
			print_error("TRY 'GIMME myvar'", self, "EOL-error")
		elif(self.states[-1] == "HOW..." or self.states[-1] == "HOW DUZ..." or self.states[-1] == "HOW DUZ I..." or
			self.states[-1] == "HOW DUZ I function..."):
			# Unfinished function declaration
			print_error("TRY 'HOW DUZ I dosomething ?'", self, "EOL-error")
		elif(self.states[-1] == "IF...'" or self.states[-1] == "IF U..." or self.states[-1] == "IF U SAY..."): 
			# Unfinished function termination
			print_error("TRY 'IF U SAY SO' TO END 'HOW DUZ I'", self, "EOL-error")
		elif(self.states[-1] == "IZ..." or self.states[-1] == "IZ var..." or self.states[-1] == "IZ var op..." or 
			self.states[-1] == "IZ var op THAN..." or self.states[-1] == "IZ var op THAN value..."):
			# Unfinished comparison
			print_error("TRY 'IZ myvar BIGR THAN 50 ?", self, "EOL-error")
		elif (self.states[-1] == "string"):
			# Unfinished string literal
			print_error("U R MISING QUOTS: U SEEZ \"HAI\"", self, "EOL-error") 
		elif (self.states[-1] == "number op..."):
			# Unfinished math expression
			print_error("WHERE IZ YR NEXT NUMBAR?", self, "EOL-error")

		# Valid states, but ones with special status
		elif (self.states[-1] == "single-line-comment"):
			self.pop_state()
			if (self.states[-1] == "number..."):
				self.pop_state()	# pop the overlying number... state
				self.pop_state()	# pop the overlyig EOL state
		elif(self.states[-1] == "I HAS A var..."):
			# Variable declared but not initialized
			self.pop_state()
			self.append_code("= 0")	# variables are 0 by default
		elif(self.states[-1] == "number..."):
			self.pop_state()		# pop the number state
			if (self.states[-1] == "EOL"):
				self.pop_state()		# pop the overlying EOL state
		elif(self.states[-1] == "EOL"):
			self.pop_state()
		self.code += "\n"
		self.line = self.word = self.curvar = ""
		self.lineno += 1

lolparser = Parser()

# ========== Read File ==========

try:
	source = open(source_path)
except IOError, e:
	print_error("IOError: " + source_path + ": " + e.strerror, lolparser, "IOerror")

# Process source code line by line
line = source.readline()
while line:
	lolparser.begin_line(line)
	for word in line.strip().replace("\t", " ").split(' '):
		lolparser.read_word(word)
	lolparser.finish_line()
	line = source.readline()

source.close()

# ========== Check End State ==========

if (lolparser.states[-1] == "initial"):
	print_error("I SEEZ NUTHIN IN YR FILE!", lolparser, "EOF-error")
elif (lolparser.states[-1] == "multi-line-comment"):
	print_error("I SEEZ 'OBTW', BUT WHERE IS 'TLDR'?", lolparser, "EOF-error")
elif (lolparser.states[-1] == "YARLY" or lolparser.states[-1] == "NOWAI"):
	print_error("PLZ SAY 'KTHX' AFTER 'YARLY' AN 'NOWAI'", lolparser, "EOF-error")
elif (lolparser.states[-1] == "function"):
	print_error("I SEEZ 'HOW DUZ I', BUT WHERE IS 'IF U SAY SO'?", lolparser, "EOF-error")
elif (lolparser.states[-1] != "end"):
	print_error("PLZ SAY 'KTHXBYE' AT END OF PROGRM! KTHX", lolparser, "EOF-error")

# ========== Execute Code or Write File ==========

try:
	dest_path = sys.argv[2]	
	dest = open(dest_path, "w")
	print >>dest, lolparser.code
	os.system("chmod u+x " + dest_path)  # make new file executable
except IndexError, e:
	# No destination file specified, run code instead
	exec(lolparser.code)
except IOError, e:
	print_error("IOError: " + dest_path + ": " + e.strerror, lolparser, "IOerror")

