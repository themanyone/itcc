# itcc - a read-eval-print loop for C/C++ programmers
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

file_boilerplate = """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
$user_includes
int main(int argc, char **argv, char **env){
$user_commands    return 0;
}"""

def get_full_source( runner ):
    return ( file_boilerplate
        .replace( "$user_commands", runner.get_user_commands_string() )
        .replace( "$user_includes", runner.get_user_includes_string() )
    )
