# izig - a read-eval-print loop for C/C++, zig, rust & hare programmers
#
# igcc Copyright (C) 2009 Andy Balaam
# with python3, rust, hare, and other support by Henry Kroll III
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

import itertools
import platform
import os
import os.path
import re
import readline
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from argparse import ArgumentParser
from colorama import init, Fore, Back

from . import dot_commands_zig as dot_commands
from . import source_code_zig as source_code
from . import version

# --------------

# One day these will be in a config file

prompt = "zig> "
compiler_command = ( "zig", "build-exe", "-o", "$lib_dirs", "$libs", "$srcfile" )

include_dir_command = ( "-I$cmd", )
lib_dir_command = ( "-L$cmd", )
lib_command = ( "-l$cmd", )

#---------------

incl_re = re.compile( r"\s*(use|extern|#\S+)\s" )

#---------------

def read_line_from_stdin( prompt ):
    try:
        return input( prompt )
    except EOFError:
        return None

def read_line_from_file( inputfile, prompt ):
    sys.stdout.write( prompt )
    line = inputfile.readline()
    if line is not None:
        print(line)
    return line

def create_read_line_function( inputfile, prompt ):
    if inputfile is None:
        return lambda: read_line_from_stdin( prompt )
    else:
        return lambda: read_line_from_file( inputfile, prompt )

def get_temporary_file_name():
    suff = ".exe" if platform.system() == 'Windows' else ""
    outfile = tempfile.NamedTemporaryFile( prefix = 'izig', suffix = suff )
    outfilename = outfile.name
    outfile.close()
    return outfilename

def append_multiple( single_cmd, cmdlist, ret ):
    if cmdlist is not None:
        for cmd in cmdlist:
            for cmd_part in single_cmd:
                ret.append(
                    cmd_part.replace( "$cmd" , cmd ) )

def get_compiler_command( options, extra_options, srcfilename, exefilename ):
    ret = []

    for part in compiler_command:
        if part == "$srcfile":
            ret.append( part.replace( "$srcfile", srcfilename ) )
        elif part == "-o":
            append_multiple( extra_options, extra_options, ret)
        elif part == "$lib_dirs":
            append_multiple( lib_dir_command, options.LIBDIR,ret )
        elif part == "$libs":
            append_multiple( lib_command, options.LIB, ret )
        else:
            ret.append( part.replace( "$outfile", exefilename ) )
    return ret


def run_compile( subs_compiler_command, runner, srcfilename ):
    compile_process = subprocess.Popen( subs_compiler_command,
        stdin = subprocess.PIPE, stderr = subprocess.PIPE )
    source = source_code.get_full_source(runner)
    if runner.options.v > 2:
        print(source)
    with open(srcfilename, 'w') as file:
        file.write(source)
        file.close()
    compile_process = subprocess.Popen( subs_compiler_command,
        stdin = subprocess.PIPE, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE )
    stdoutdata, stderrdata = compile_process.communicate()

    if compile_process.returncode == 0:
        return None
    elif stdoutdata is not None:
        if stderrdata is not None:
            return stdoutdata + stderrdata
        else:
            return stdoutdata
    else:
        if stderrdata is not None:
            return stderrdata
        else:
            return "Unknown compile error - compiler did not write any output."

def run_exe( exefilename, extra_args ):
    run_process = subprocess.Popen([ exefilename, *extra_args],
        stdout = subprocess.PIPE, stderr = subprocess.PIPE )
    return run_process.communicate()

def print_welcome():
    print(f'''izig $version
{Back.BLACK}{Fore.GREEN}Released under GNU GPL version 2 or later, with NO WARRANTY.
Get zig from{Fore.BLUE} https://ziglang.org/
{Fore.RESET}Type ".h" for help.{Back.RESET}
'''.replace( "$version", version.VERSION ))

class UserInput:
    INCLUDE = 0
    COMMAND = 1

    def __init__( self, inp, typ ):
        self.inp = inp
        self.typ = typ
        self.output_chars = 0
        self.error_chars = 0

    def __str__( self ):
        return "UserInput( '%s', %d, %d, %d )" % (
            self.inp, self.typ, self.output_chars, self.error_chars )

    def __eq__( self, other ):
        return (
            self.inp == other.inp and
            self.typ == other.typ and
            self.output_chars == other.output_chars and
            self.error_chars == other.error_chars )

    def __ne__( self, other ):
        return not self.__eq__( other )

class Runner:

    def __init__( self, options, extra_options, inputfile, srcfilename, exefilename ):
        self.options = options
        self.extra_options = extra_options
        self.inputfile = inputfile
        self.srcfilename = srcfilename
        self.exefilename = exefilename
        self.user_input = []
        self.input_num = 0
        self.compile_error = ""
        self.output_chars_printed = 0
        self.error_chars_printed = 0

    def do_run( self, session_args ):
        read_line = create_read_line_function( self.inputfile, prompt )
        subs_compiler_command = get_compiler_command(
            self.options, self.extra_options, self.srcfilename, self.exefilename )

        inp = 1
        while inp is not None:
            inp = read_line()
            if inp is not None:

                col_inp, run_cmp = (
                    dot_commands.process( inp, self ) )
                if col_inp:
                    if self.input_num < len( self.user_input ):
                        self.user_input = self.user_input[ : self.input_num ]
                        self.user_input.append( UserInput( "    " + inp, typ ) )
                    if incl_re.match( inp ):
                        typ = UserInput.INCLUDE
                        self.user_input.append( UserInput( inp, typ ) )
                    else:
                        typ = UserInput.COMMAND
                        self.user_input.append( UserInput( "    " + inp, typ ) )
                    self.input_num += 1

                if run_cmp:
                    # print compiler command
                    if self.options.v > 1:
                        print("$ " + ( " ".join( subs_compiler_command ) ))
                    os.chdir("/tmp")
                    self.compile_error = run_compile( subs_compiler_command,
                    self, self.srcfilename )

                    if self.compile_error is not None:
                        err = self.compile_error.decode().strip('\n')
                        if self.options.v > 2:
                            print(err)
                        # ignore some compiler errors
                        elif (err.find("unused local") < 0
                          and err.find("found 'eof'") < 0
                          and err.find("found '}'") < 0
                          and err.find("end of file") < 0) or self.options.e:
                            print("[Compile error - type .e to see it.]")
                    else:
                        if self.options.v > 0:
                            print("session_args:", *session_args)
                        stdoutdata, stderrdata = run_exe( self.exefilename,
                            session_args )

                        if len( stdoutdata ) > self.output_chars_printed:
                            new_output = stdoutdata[self.output_chars_printed:]
                            len_new_output = len( new_output )
                            print(new_output.decode().strip('\n'))
                            self.output_chars_printed += len_new_output
                            self.user_input[ -1 ].output_chars = len_new_output

                        if len( stderrdata ) > self.error_chars_printed:
                            new_error = stderrdata[self.error_chars_printed:]
                            len_new_error = len( new_error )
                            print(new_error.decode().strip('\n'))
                            self.error_chars_printed += len_new_error
                            self.user_input[ -1 ].error_chars = len_new_error

        print()

    def redo( self ):
        if self.input_num < len( self.user_input ):
            self.input_num += 1
            return self.user_input[ self.input_num - 1 ].inp
        else:
            return None


    def undo( self ):
        if self.input_num > 0:
            self.input_num -= 1
            undone_input = self.user_input[ self.input_num ]
            self.output_chars_printed -= undone_input.output_chars
            self.error_chars_printed -= undone_input.error_chars
            return undone_input.inp
        else:
            return None

    def get_user_input( self ):
        return itertools.islice( self.user_input, 0, self.input_num )

    def get_user_commands( self ):
        return ( a.inp for a in filter(
            lambda a: a.typ == UserInput.COMMAND,
            self.get_user_input() ) )

    def get_user_includes( self ):
        return ( a.inp for a in filter(
            lambda a: a.typ == UserInput.INCLUDE,
            self.get_user_input() ) )

    def get_user_commands_string( self ):
        return "\n".join( self.get_user_commands() ) + "\n"

    def get_user_includes_string( self ):
        return "\n".join( self.get_user_includes() ) + "\n"

def parse_args( argv ):
    parser = ArgumentParser()
    parser.description =\
        "Run an interactive Zig live coding session."
    parser.add_argument( "-v", action="count", default=0,
        help = "Increase verbosity." )
    parser.add_argument( "-e", action="store_true",
        help = "Show errors about empty blocks." )
    parser.add_argument( "-I", dest="INCLUDE", action="append",
        help = "Add INCLUDE to the list of directories to " +
            "be searched for header files." )
    parser.add_argument( "-L", dest="LIBDIR", action="append",
        help = "Add LIBDIR to the list of directories to " +
            "be searched for library files." )
    parser.add_argument( "-l", dest="LIB", action="append",
        help = "Search the library LIB when linking." )
    parser.add_argument( "-compiler_args", action="store_true",
        help = "Any compiler args can go here.")
    parser.add_argument( "--", nargs="+", dest="session_args",
         help="After -- args go into my interactive session's argv[].");

    options, args = parser.parse_known_args(argv)

    # Separate args and compiler args
    # We could have argparse do this but the help output is confusing.
    separator_index = args.index('--') \
        if '--' in args else len(args)
    extra_compiler_args = args[:separator_index]
    session_args = args[separator_index + 1:]

    return options, extra_compiler_args, session_args

def run( outputfile = sys.stdout, inputfile = None, print_welc = True,
        argv = None ):
    exefilename = ""

    # Use a with statement block to redirect sys.stdout
    with redirect_stdout(outputfile):
        #try:
        options, extra_args, session_args = parse_args(argv)

        exefilename = get_temporary_file_name()
        srcfilename = exefilename + ".zig"
        ret = "normal"
        if print_welc:
            print_welcome()
        Runner(options, extra_args, inputfile, srcfilename, exefilename).do_run(session_args)
        #except Exception as e:
        #    print(e)
        #    ret = "quit"

    if os.path.isfile(exefilename): # never happens
        os.remove(exefilename)
    if os.path.isfile(srcfilename):
        os.remove(srcfilename)

    return ret
