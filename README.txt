LOLcat - README
Austin Byers, 2013


Overview
-------------------------
The lolcat is a python program that parses LOLCODE and translates it into python. Here is a snippet of LOLCODE:

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

All of the keywords come from the lol cats trolling the internet!

It should be noted that I created a slightly different version of LOLCODE than the "original." 

The goal of this program was not just to parse LOLcode, but to catch every syntax error while doing so, just like a real compiler would. To that end, lolcat parses LOLCODE using a finite state automaton (in much the same way as most other advanced language parsers). The parser also uses various stacks in order to keep track of the current context of the parsed code.

Note that this was written in 3 days for an undergraduate computer science final (so cut me some slack!) The language is Turing complete, but it is the bare minimum! For example, who needs loops and method return values when you can just have recursion and global variables? lol

There is even a language specification file for gedit, so that you can get syntax highlighting! So forget Python, now you can program everything in LOLCODE! Your teachers and coworkers will thank you for it.


Included Files
-------------------------
 - lolcat.py: the python program for translating LOLCODE
 - help.txt: explains how to use LOLCODE. It can be printed with "./lolcat.py --help"
 - lol.lang: a language specification file for syntax highling in gedit and other gtksourceview programs. On most distros you can just copy this to /usr/share/gtksourceview-3.0/language-specs/lolcode.lang
 - fib.lol: an example LOLCODE file which prints all the numbers of the fibonacci sequence in a given range
 - fib.py: the python translation of the fib.lol file produced by the lolcat parser. 


License
-------------------------
This can be used for anything you want; all I ask is that you give credit where credit is due!
