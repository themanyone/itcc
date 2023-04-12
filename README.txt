Interactive TCC
===============

A real-eval-print loop (REPL) for C/C++ programmers, written in Python.

Interactive TCC (itcc) is a python3 fork of Interactive GCC (igcc) https://codeberg.org/andybalaam/igcc with TCC compiler option.

Get optional TCC compiler here:
 git clone https://repo.or.cz/tinycc.git/

The advantage of using TCC is speed. There are no compiler delays between entering code and seeing the results! But it lacks some of the functionality of GCC. Also, TCC is a C compiler, not a C++ compiler like GCC.

Use Interactive TCC for C programming, like this:

 $ ./itcc
 tcc> int a = 5;
 tcc> a -= 2;
 tcc> if (a < 4) {
 ['-:16: error: identifier expected']
 tcc>    printf("a is %i\n", a);
 ['-:17: error: identifier expected']
 tcc> }
 a is 3

Ignore errors. The result is printed after typing the closing brace "}".

Tired of typing all those semicolons and parenthesis? Crap coding is also supported. Crap is a light-weight wrapper around standard C code. https://themanyone.github.io/crap/

 $ ./icrap
 crap> puts  "hi"
 hi
 crap> for  int x=3;x--;
 crap>     printf  "x is %i\n", x
 x is 2
 x is 1
 x is 0

Interactive TCC works about like Interactive GCC (igcc), which is also included in this package. If you can convert C++ to C, you might even be able to struggle through some of following examples using itcc.
 
Interactive GCC
===============

Use Interactive GCC for C++ programming, like this:

 $ ./igcc 
 g++> int a = 5;
 g++> a += 2;
 g++> cout << a << endl;
 7
 g++> --a;
 g++> cout << a << endl;
 6
 g++> 

It is possible to include header files you need like this:

 $ ./igcc 
 g++> #include <vector>
 g++> vector<int> myvec;
 g++> myvec.push_back( 17 );
 g++> printf( "%d\n", myvec.size() );
 1
 g++> myvec.push_back( 21 );
 g++> printf( "%d\n", myvec.size() );
 2
 g++> 

Compile errors can be tolerated until the code works:

 $ ./igcc
 g++> #include <map>
 g++> map<string,int> hits;
 g++> hits["foo"] = 12;
 g++> hits["bar"] = 15;
 g++> for( map<string,int>::iterator it = hits.begin(); it != hits.end(); ++it )
 [Compile error - type .e to see it.]
 g++> {
 [Compile error - type .e to see it.]
 g++> 	cout << it->first << " " << it->second << endl;
 [Compile error - type .e to see it.]
 g++> }
 bar 15
 foo 12
 g++> 

Extra include directories can be supplied:

 $ ./igcc -Itest/cpp -Itest/cpp2
 g++> #include "hello.h"
 g++> hello();
 Hello, 
 g++> #include "world.h"
 g++> world();
 world!
 g++> 

Libs can be linked:

 $ ./igcc -lm
 g++> #include "math.h"
 g++> cout << pow( 3, 3 ) << endl; // Actually a bad example since libm.a is already linked in C++
 27
 g++> 

Your own libs can be linked too:

 $ ./igcc -Itest/cpp -Ltest/cpp -lmylib
 g++> #include "mylib.h"
 g++> defined_in_cpp();
 defined_in_cpp saying hello.
 g++> 

The cstdio, iostream and string headers are automatically included, and the std namespace is automatically in scope.

Downloading and using
---------------------

Download the IGCC tarball from the Sourceforge download area:

https://sourceforge.net/projects/igcc/files/

Untar it like so:

 tar -xjf igcc-0.1.tar.bz2

And then start the program like this:

 cd igcc-0.1
 ./igcc

Then type the C++ code you want to execute. It will be compiled with GCC and the results (if any) will be displayed.

Type .h to see some general help on usage.

Type .h followed by the command name for more help:

 .h printf
 .h string
 .h glob

Developing
----------

IGCC is a small python wrapper around GCC.

Check out the code here:

 git clone git://igcc.git.sourceforge.net/gitroot/igcc/igcc

Or browse the source here:

http://igcc.git.sourceforge.net/git/gitweb.cgi?p=igcc/igcc;a=tree

Links
-----

IGCC home page:
http://www.artificialworlds.net/wiki/IGCC/IGCC

IGCC Sourceforge page:
http://sourceforge.net/projects/igcc/

Andy Balaam's home page:
http://www.artificialworlds.net

Andy Balaam's blog:
http://www.artificialworlds.net/blog

Contact
-------

Andy Balaam may be contacted on axis3x3 at users dot sourceforge dot net

Copyright
---------

IGCC is Copyright (C) 2009 Andy Balaam

IGCC is Free Software released under the terms of the GNU General Public License version 2 or later.

IGCC comes with NO WARRANTY.

See the file COPYING for more information.

