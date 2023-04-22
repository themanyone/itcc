Interactive TCC
===============

A read-eval-print loop (REPL) for C/C++ programmers, written in Python.

Interactive TCC (itcc) is a python3 fork of Interactive GCC (igcc) with TCC compiler option. Get it from GitHub https://github.com/themanyone/itcc

Get TCC compiler here:
 git clone https://repo.or.cz/tinycc.git/

The advantage of using TCC is speed. There are no compiler delays between entering code and seeing the results! But it lacks some of the functionality of GCC. Also, TCC is a C compiler, not a C++ compiler like GCC.

Use the Interactive TCC shell, like this:

 $ ./itcc
 tcc> int a = 5;
 tcc> a -= 2;
 tcc> if (a < 4) {
 ['-:16: error: identifier expected']
 tcc>    printf("a is %i\n", a);
 ['-:17: error: identifier expected']
 tcc> }
 a is 3
 tcc> |

Ignore errors. The result is printed after typing the closing brace "}".

Interactive Crap
================

Tired of typing all those semicolons, curly braces, and parenthesis? Want to indent instead, like Python but still produce valid C code? Crap coding is also supported. Crap is a light-weight wrapper around standard C. And since braces are added automatically, there might be fewer errors. Get crap from https://themanyone.github.io/crap/

 $ ./icrap -lm
 crap> #include "math.h"
 crap> for  int x=0;x<5;x++
 crap>      printf  "%i squared is %0.0f\n", x, pow(x, 2.0)
 0 squared is 0
 1 squared is 1
 2 squared is 4
 3 squared is 9
 4 squared is 16
 crap> |

Interactive TCC works about like the original Interactive GCC (igcc), which is also included in this package. If you can convert C++ to C, you might even be able to struggle through some of following examples using itcc, or icrap.

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
 g++> |

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
 g++> |

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
 g++> |

Libs can be linked:

 $ ./igcc -lm
 g++> #include "math.h"
 g++> cout << pow( 3, 3 ) << endl; // Actually a bad example since libm.a is already linked in C++
 27
 g++> |

Your own libs can be linked too:

 $ ./igcc -Itest/cpp -Ltest/cpp -lmylib
 g++> #include "mylib.h"
 g++> defined_in_cpp();
 defined_in_cpp saying hello.
 g++> |

The cstdio, iostream and string headers are automatically included, and the std namespace is automatically in scope.

FAQ. Issues.
============

How does it work? Does it re-run the entire code block each time?

Yes. Although it runs all the code each time, it only prints the new output. Supposedly. There appears to be some bugs with detecting what was already printed, causing some new lines to produce no output. In that case, just restart it. We're working on that...

Downloading and using
---------------------
itcc is published on GitHub. Get it from https://github.com/themanyone/itcc

For Python2, you may opt to download Andy Balaam's original IGCC tarball from the Sourceforge download area:

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

 git clone https://github.com/themanyone/itcc.git

Or browse the source here:

https://github.com/themanyone/itcc

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

