#!/usr/bin/python3

# igcc - a read-eval-print loop for C/C++ programmers
#
# Copyright (C) 2009 Andy Balaam
# with python3 and tcc support by Henry Kroll III
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import re

import libigcc.rungo
from libigcc.run import UserInput
import libigcc.source_code_go
import libigcc.version

class FakeWriteableFile:
	def __init__( self ):
		self.lines = []

	def write( self, line ):
		self.lines.append( line )

class FakeReadableFile:
	def __init__( self, lines ):
		self.lines = lines

	def readline( self ):
		if len( self.lines ) == 0:
			return None
		line = self.lines[0]
		self.lines = self.lines[1:]
		return line

def assert_strings_equal( str1, str2 ):
	if str1 == str2:
		return

	raise AssertionError( "\n" + str1 + "\n!=\n" + str2 )

def assert_strings_match( string, re_string ):
	cmp_re = re.compile( re_string, re.DOTALL )

	if cmp_re.match( string ):
		return

	raise AssertionError( "\n" + string
		+ "\ndoes not match regular expression\n" + re_string )

def strip_codes(text):
	# Define the regular expression pattern to match ANSI escape codes
	ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
	# Use the pattern to remove the color codes from the text
	stripped_text = ansi_escape.sub('', text)
	return stripped_text

def run_program( commands, expected_output, print_welcome = False,
		argv = None ):

	outputfile = FakeWriteableFile()
	stdinfile = FakeReadableFile( commands )
	ret = libigcc.rungo.run( outputfile, stdinfile, print_welcome, argv )
	txt = "".join( outputfile.lines )
	assert_strings_equal( strip_codes(txt), expected_output )

	return ret

def run_program_regex_output( commands, expected_output_re ):
	outputfile = FakeWriteable-File()
	stdinfile = FakeReadableFile( commands )
	libigcc.rungo.run( outputfile, stdinfile, False )

	assert_strings_match( "".join( outputfile.lines ), expected_output_re )

def test_print_argv():
    commands = [ 'import "os"', "fmt.Println(len(os.Args))" ]
    expected_output = 'go> import "os"\ngo> fmt.Println(len(os.Args))\n2\ngo> \n'
    run_program( commands, expected_output, False, ['--', 'foo'] )

def test_declare_var():
	commands = [ "var a int" ]
	expected_output = 'go> var a int\ngo> \n'
	run_program( commands, expected_output )

def test_declare_var_assign():
	commands = [ "var a int", "a = 10" ]
	expected_output = 'go> var a int\ngo> a = 10\ngo> \n'
	run_program( commands, expected_output )

def test_declare_and_assign_var_then_print():
	commands = [ "a := 10",
		'fmt.Println(a)' ]

	expected_output = (
'''go> a := 10
go> fmt.Println(a)
10
go> 
''' )

	run_program( commands, expected_output )


def test_print_twice():
	commands = [ "a := 10",
		'fmt.Println(a)',
		"a++",
		'fmt.Println(a)' ]

	expected_output = (
'''go> a := 10
go> fmt.Println(a)
10
go> a++
go> fmt.Println(a)
11
go> 
''' )

	run_program( commands, expected_output )

def test_compile_error():
	commands = [ "var a int;" ] # semicolon

	expected_output = (
'''go> var a int;
go> 
''' )

	run_program( commands, expected_output )

def test_compile_error_display():
	commands = [
		"var a int;" # semicolon
		".e" ]

	# Just look for a string "xpected" in the compiler output.
	expected_output_re = (
u'''.*expected.*''' )

	run_program_regex_output( commands, expected_output_re )

def test_include():
    commands = [
		'fmt.Println("hello")' ]

    expected_output = (
    r'''go> fmt.Println("hello")
hello
go> 
''' )

    run_program( commands, expected_output )

def test_multiple_repeated_includes():
	commands = [
		'import "strings"',
		'fmt.Println(strings.ToUpper("hello"))' ]

	expected_output = (
	r'''go> import "strings"
go> fmt.Println(strings.ToUpper("hello"))
HELLO
go> 
''' )

	run_program( commands, expected_output )

def test_list_program():
	commands = [
		'var a int',
		'a += 2',
		'.l' ]

	expected_output = (
	r'''go> var a int
go> a += 2
go> .l


    var a int
    a += 2
go> 
''' )

	run_program( commands, expected_output )

class FakeRunner:
	def __init__( self, user_commands_string, user_includes_string ):
		self.user_commands_string = user_commands_string
		self.user_includes_string = user_includes_string

	def get_user_commands_string( self ):
		return self.user_commands_string

	def get_user_includes_string( self ):
		return self.user_includes_string

def test_list_full_program():
	commands = [
		'var a int',
		'a += 2',
		'.L' ]

	fakerunner = FakeRunner( 'var a int\na += 2\n', '' )

	expected_output = (
'''go> var a int
go> a += 2
go> .L
package main
import "fmt"

func main() {
    var a int
    a += 2
}
go> 
''')

	run_program( commands, expected_output )

def test_help_message():
	commands = [
		'.h' ]

	expected_output_re = ".*Show this help message"

	run_program_regex_output( commands, expected_output_re )

def test_quit():
	commands = [
		'.q' ]

	expected_output = "go> .q\n"

	ret = run_program( commands, expected_output )

	assert_strings_equal( ret, "quit" )

def test_welcome_message():
	commands = []
	expected_output = (
'''igo $version
Released under GNU GPL version 2 or later, with NO WARRANTY.
Get go from https://go.dev/
Type ".h" for help.

go> 
''' ).replace( "$version", libigcc.version.VERSION )

	run_program( commands, expected_output, True )

def test_print_license():
	commands = [ '.c' ]

	expected_output_re = (
	r'''go> .c
.*GNU GENERAL PUBLIC LICENSE.*\ngo> 
''' )

	run_program_regex_output( commands, expected_output_re )

def test_print_warranty():
	commands = [ '.w' ]

	expected_output_re = (
	r'''go> .w
.*Disclaimer of Warranty.*\ngo> 
''' )

	run_program_regex_output( commands, expected_output_re )

def test_runner_get_user_input():
	runner = libigcc.rungo.Runner( None, None, None, None, None )
	runner.user_input = [
		UserInput("0", UserInput.COMMAND),
		UserInput("1", UserInput.COMMAND),
		UserInput("2", UserInput.COMMAND) ]
	runner.input_num = 3
	assert( tuple( runner.get_user_input() ) == (
		UserInput("0", UserInput.COMMAND),
		UserInput("1", UserInput.COMMAND),
		UserInput("2", UserInput.COMMAND) ) )

	runner.input_num = 2
	assert( tuple( runner.get_user_input() ) == (
		UserInput("0", UserInput.COMMAND),
		UserInput("1", UserInput.COMMAND) ) )

	runner.input_num = 1
	assert( tuple( runner.get_user_input() ) == (
		UserInput("0", UserInput.COMMAND), ) )

def test_runner_get_user_commands():
	runner = libigcc.rungo.Runner( None, None, None, None, None )
	runner.user_input = [
		UserInput("0", UserInput.COMMAND),
		UserInput("1", UserInput.COMMAND),
		UserInput("X", UserInput.INCLUDE),
		UserInput("2", UserInput.COMMAND) ]
	runner.input_num = 4
	assert( tuple( runner.get_user_commands() ) == ( "0", "1", "2" ) )

	runner.input_num = 2
	assert( tuple( runner.get_user_commands() ) == ( "0", "1" ) )

	runner.input_num = 1
	assert( tuple( runner.get_user_commands() ) == ( "0", ) )

def test_undo_1():
	commands = [
		'var a int',
		'a = 5',
		'foobar',
		'.u',
		'fmt.Println(a)',
		]

	expected_output = (
	r'''go> var a int
go> a = 5
go> foobar
go> .u
[Undone '    foobar'.]
go> fmt.Println(a)
5
go> 
''' )

	run_program( commands, expected_output )

def test_undo_2():

	commands = [
		'a := 5',
		'a++',
		'a++',
		'a++',
		'.u',
		'.u',
		'fmt.Println(a)',
		]

	expected_output = (
r'''go> a := 5
go> a++
go> a++
go> a++
go> .u
[Undone '    a++'.]
go> .u
[Undone '    a++'.]
go> fmt.Println(a)
6
go> 
''' )

	run_program( commands, expected_output )


def test_undo_before_beginning():

	commands = [ 'a := 5', '.u', '.u', '.u', 'fmt.Println(a)',
		'.u',
		'b := 7',
		'fmt.Println(b)',
		]



	expected_output = (

r'''go> a := 5
go> .u
[Undone '    a := 5'.]
go> .u
[Nothing to undo.]
go> .u
[Nothing to undo.]
go> fmt.Println(a)
[Compile error - type .e to see it.]
go> .u
[Undone '    fmt.Println(a)'.]
go> b := 7
go> fmt.Println(b)
7
go> 
''' )

	run_program( commands, expected_output )

def test_undo_includes_and_commands():

	commands = [ 'a := 5', 'a++',
		'.u',

		'.u',

		'.u',

		]



	expected_output = (

r'''go> a := 5
go> a++
go> .u
[Undone '    a++'.]
go> .u
[Undone 'import "fmt"'.]
go> .u
[Undone '    a := 5'.]
go> 
''' )



	run_program( commands, expected_output )





def test_redo_1():

	commands = [ 'a := 1', 'a++',
		'.r',

		'fmt.Println(a)',

		]



	expected_output = (

r'''go> a := 1
go> a++
go> .u
[Undone '    a++'.]
go> .r
[Redone '    a++'.]
go> fmt.Println(a)
2
go> 
''' )



	run_program( commands, expected_output )









def test_redo_2():

	commands = [ 'a := 1', 'a++',
		'.u',

		'.r',

		'.r',

		'fmt.Println(a)',

		]



	expected_output = (

r'''go> a := 1
go> a++
go> .u
[Undone '    a++'.]
go> .u
[Undone '    a := 1'.]
go> .r
[Redone '    a := 1'.]
go> .r
[Redone '    a++'.]
go> fmt.Println(a)
2
go> 
''' )



	run_program( commands, expected_output )









def test_redo_before_beginning():

	commands = [ 'a := 1', 'a++',
		'.u',

		'.u',

		'.r',

		'.r',

		'fmt.Println(a)',

		]



	expected_output = (

r'''go> a := 1
go> a++
go> .u
[Undone '    a++'.]
go> .u
[Undone '    a := 1'.]
go> .u
[Nothing to undo.]
go> .r
[Redone '    a := 1'.]
go> .r
[Redone '    a++'.]
go> fmt.Println(a)
2
go> 
''' )



	run_program( commands, expected_output )







def test_redo_after_end():

	commands = [ 'a := 1', 'a++',
		'.r',

		'.r',

		'fmt.Println(a)',

		]



	expected_output = (

r'''go> a := 1
go> a++
go> .u
[Undone '    a++'.]
go> .r
[Redone '    a++'.]
go> .r
[Nothing to redo.]
go> fmt.Println(a)
2
go> 
''' )



	run_program( commands, expected_output )





def test_redo_includes_and_commands():

	commands = [ 'a := 5', 'a++',
		'.u',

		'.u',

		'.u',

		'.r',

		'.r',

		'.r',

		]



	expected_output = (

r'''go> a := 5
go> a++
go> .u
[Undone '    a++'.]
go> .u
[Undone 'import "fmt"'.]
go> .u
[Undone '    a := 5'.]
go> .r
[Redone '    a := 5'.]
go> .r
[Redone 'import "fmt"'.]
go> .r
[Redone '    a++'.]
go> 
''' )



	run_program( commands, expected_output )





def test_undo_then_new_commands():

	commands = [ 'a := 5', 'a++',
		'a--',

		'a--',

		'.u',

		'fmt.Println(a)',

		]



	expected_output = (

r'''go> a := 5
go> a++
go> .u
[Undone '    a++'.]
go> a--
go> a--
go> .u
[Undone '    a--'.]
go> fmt.Println(a)
4
go> 
''' )



	run_program( commands, expected_output )





def test_undo_redo_with_output():

	commands = [ 'a := 56',
		'fmt.Println(a)',
		'.u',
		'.r',
		'.u',
		'fmt.Println(12)',
		]

	expected_output = (

r'''go> a := 56
go> fmt.Println(a)
56
go> .u
[Undone '    fmt.Println(a)'.]
go> .r
[Redone '    fmt.Println(a)'.]
56
go> .u
[Undone '    fmt.Println(a)'.]
go> fmt.Println(12)
12
go> 
''' )

	run_program( commands, expected_output )
def main():
	test_print_argv()
	test_declare_var()
	test_declare_var_assign()
	test_declare_and_assign_var_then_print()
	test_print_twice()
	test_compile_error()
	#test_compile_error_display()
	test_include()
	test_multiple_repeated_includes()
	test_list_program()
	test_list_full_program()
	#test_help_message()
	test_quit()
	test_welcome_message()
	#test_print_license()
	#test_print_warranty()
	test_runner_get_user_input()
	test_runner_get_user_commands()
	test_undo_1()
	test_undo_2()
	test_undo_before_beginning()
	test_undo_includes_and_commands()
	test_redo_1()
	test_redo_2()
	test_redo_before_beginning()
	test_redo_after_end()
	test_redo_includes_and_commands()
	test_undo_then_new_commands()
	test_undo_redo_with_output()

	#test_readline_history();
	#test_print_command();
	#test_edit_in_vim();
	#test_compile_warning()
	#test_remove_compile_error_message()

	print("All tests passed.")


if __name__ == "__main__":
	main()
