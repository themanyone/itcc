# izig - a read-eval-print loop for C/C++, hare & rust programmers
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

from . import source_code_zig as source_code
from . import copying
import subprocess
import os
from glob import glob

# documentation search paths
home = os.environ.get('HOME')
docs_url = 'https://ziglang.org/documentation/0.11.0/'

class IGCCQuitException(Exception):
    pass

def highlight( code ):
    cmd = "highlight -f -S zig -O xterm256 -"
    print_proc = subprocess.Popen( cmd, shell=True, 
    stdin = subprocess.PIPE, stdout = subprocess.PIPE )
    stdout, stderr = print_proc.communicate(code.encode())
    print(stdout.decode("utf-8").strip())

def dot_c( runner ):
    print(copying.copying)
    return False, False

def dot_e( runner ):
    if runner is not None and hasattr(runner.compile_error, "decode"):
        print(runner.compile_error.decode().strip('\n'))
    return False, False

def dot_f( runner ):
    print("Function entry mode. Enter a blank line to finish. CTRL-C to cancel.")
    input_list = []
    try:
        while True:
            line = input().replace('\t', '    ')
            if not line: break
            input_list.append(line)
        runner.inp = "\n".join(input_list)
    except KeyboardInterrupt:
        return False, False
    # return yes we want to input the function, but no to compiling it
    return True, False

def dot_g( runner ):
    cmd = "man -k library | highlight --force=rust -O xterm256"
    run_process = subprocess.Popen( cmd, shell=True )
    run_process.wait()
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

def dot_v( runner ):
    run_process = subprocess.Popen(["xdg-open", docs_url],
    stdout = subprocess.PIPE, stderr = subprocess.PIPE )
    stdout, stderr = run_process.communicate()
    return False, False

def dot_w( runner ):
    print(copying.warranty)
    return False, False

dot_commands = {
    ".c" : ( "Show copying information", dot_c ),
    ".e" : ( "Show the last compile errors/warnings", dot_e ),
    ".f" : ( "Function or top-level declaration", dot_f ),
    ".g" : ( "Get list of c libraries to show man pages about", dot_g ),
    ".h" : ( "Show this help message", None ),
    ".h [lib]" : ("Show help about zig [lib]", None ),
    ".q" : ( "Quit", dot_q ),
    ".l" : ( "List the code you have entered", dot_l ),
    ".L" : ( "List the whole program as given to the compiler", dot_L ),
    ".m [lib]" : ( "Show man page about [cmd or lib]", None ),
    ".r" : ( "Redo undone command", dot_r ),
    ".s" : ( "Show list of zig libs to view help about", None ),
    ".u" : ( "Undo previous command", dot_u ),
    ".v" : ( "View Language Documentation", dot_v ),
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
    # source-highlight -s c --out-format=esc -i `find /usr/lib/zig -name *atan.zig | pick`
    if inp[:3] == ".h ":
        find = ["find", "/usr/lib/zig", "-name", f"*{inp[3:]}.zig"]
        pick = ["pick"]
        pick_process = subprocess.Popen(pick,
        stdout = subprocess.PIPE, stdin = subprocess.PIPE )
        find_process = subprocess.Popen(find,
        stdout = pick_process.stdin, stderr = subprocess.PIPE )
        stdout, stderr = pick_process.communicate()
        if find_process.stderr is not None:
            print(find_process.stderr)
        f = stdout.decode("utf-8").strip()
        view = f"highlight --syntax=c -O ansi {f}| more"
        print(view)
        view_process = subprocess.Popen(view, shell=True)
        view_process.wait()
        return False, False
    elif inp == ".s":
        find = ["find", "/usr/lib/zig", "-name", "*.zig"]
        find_process = subprocess.Popen(find,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE )
        stdout, stderr = find_process.communicate()
        libs = stdout.decode("utf-8").split("\n")
        libs = [os.path.basename(line).strip(".zig") for line in libs]
        libs = "\t".join(libs)
        print(f"""
Searchable Zip Libraries

{libs}
""")
        return False, False
    elif inp[:3] == ".m ":
        view = f"man {inp[3:]}|highlight -S c -O xterm256 -"
        run_process = subprocess.Popen(view, shell=True)
        run_process.wait()
        return False, False
    for cmd in sorted( dot_commands.keys() ):
        if inp == cmd:
            return dot_commands[cmd][1]( runner )

    return True, True
