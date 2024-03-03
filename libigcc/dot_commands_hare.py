# ihare - a read-eval-print loop for C/C++, hare programmers
#
# Copyright (C) 2009 Andy Balaam
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

from . import source_code_hare as source_code
from . import copying
import subprocess

class IGCCQuitException(Exception):
    pass

def highlight( code ):
    cmd = "highlight --syntax=c -O ansi"
    print_proc = subprocess.Popen( cmd, shell=True, 
    stdin = subprocess.PIPE, stdout = subprocess.PIPE )
    stdout, stderr = print_proc.communicate(code.encode())
    print(stdout.decode("utf-8"))

def dot_c( runner ):
    print(copying.copying)
    return False, False

def dot_e( runner ):
    if runner is not None and hasattr(runner.compile_error, "decode"):
        print(runner.compile_error.decode().strip('\n'))
    return False, False

def dot_q( runner ):
    raise IGCCQuitException()

def dot_l( runner ):
    highlight("%s\n\n    %s" % ( runner.get_user_includes_string().strip(), runner.get_user_commands_string().strip() ))
    return False, False

def dot_L( runner ):
    highlight(source_code.get_full_source( runner ))
    return False, False

def dot_r( runner ):
    redone_line = runner.redo()
    if redone_line is not None:
        print("[Redone '%s'.]" % redone_line)
        return False, True
    else:
        print("[Nothing to redo.]")
        return False, False

def dot_u( runner ):
    undone_line = runner.undo()
    if undone_line is not None:
        print("[Undone '%s'.]" % undone_line)
    else:
        print("[Nothing to undo.]")
    return False, False

def dot_w( runner ):
    print(copying.warranty)
    return False, False

dot_commands = {
    ".c" : ( "Show copying information", dot_c ),
    ".e" : ( "Show the last compile errors/warnings", dot_e ),
    ".h" : ( "Show this help message", None ),
    ".h [lib]" : ( "Show help about hare [lib]", None ),
    ".s" : ( "Show list of lib names to use", None ),
    ".q" : ( "Quit", dot_q ),
    ".l" : ( "List the code you have entered", dot_l ),
    ".L" : ( "List the whole program as given to the compiler", dot_L ),
    ".r" : ( "Redo undone command", dot_r ),
    ".u" : ( "Undo previous command", dot_u ),
    ".w" : ( "Show warranty information", dot_w ),
    }

def case_insensitive_string_compare( str1, str2 ):
    return cmp( str1.lower(), str2.lower() )

def dot_h( runner ):
    for cmd in sorted( dot_commands.keys()):
        print(cmd, dot_commands[cmd][0])
    return False, False

def process( inp, runner ):
    if inp == ".h":
        return dot_h( runner )
    elif inp[:3] == ".h ":
        run_process = subprocess.Popen(["haredoc", inp[3:]],
        stdout = subprocess.PIPE, stderr = subprocess.PIPE )
        stdout, stderr = run_process.communicate()
        highlight(stdout.decode("utf-8"))
        return False, False
    elif inp == ".s":
        print("""
Hare Standard Libraries

ascii\tbufio\tbytes\tcmd_hare_build\tcmd_hare\tcrypto_math\t
crypto_sha256\tdirs\tencoding_hex\tencoding_utf8\tendian\terrors\t
fmt\tformat_elf\tfs\tgetopt\thare_ast\thare_lex\thare_module\t
hare_parse\thare_unparse\thash\tio\tlinux\tlinux_vdso\tmath\tmemio\t
os_exec\tos\tpath\trt\tshlex\tsort_cmp\tsort\tstrconv\tstrings\t
time_chrono\ttime_date\ttime\ttypes_c\ttypes\tunix\tunix_signal\t
unix_tty

Type '.h time' for help about time.
Type '.h time::date' for submodule date.
""")
        return False, False
    for cmd in sorted( dot_commands.keys() ):
        if inp == cmd:
            return dot_commands[cmd][1]( runner )

    return True, True
