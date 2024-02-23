Interactive TCC
===============

Make programming more like Python. Now with Rust support!

An command-line shell for C, C++, Rust, and the concise, regex-aware CPP (CRAP). Also known as an evaluation context, or read-eval-print loop (REPL), the shell allows programers to type commands and see immediate results.

About this project. Interactive TCC (itcc) is a small python3 project originally forked from Interactive GCC (igcc). And we keep adding other languages as well. Get it from GitHub https://github.com/themanyone/itcc For a somewhat similar exercise in the browser, checkout https://repl.it or https://rextester.com

Depedencies. Get the optional TINYCC compiler (tcc) here (or skip down to the C++ section ad use GCC). The experimntal MOB branch of tcc accepts random contributions from anyone, so check it over carefully! Join the mailing list and check back often. git clone https://repo.or.cz/tinycc.git/

The main reason we like tcc is compilation speed. Owing to its small download size, and the smallness of the resulting executables, tcc's one-pass build ensures virtually no compiler delays between entering code and seeing the results! Tcc supports Windows, Linux, Android and other targets with many common GCC extensions. But it might lack some of the optimizations of GCC. Also, tcc is a C compiler, not a C/C++ compiler suite like GCC.

Use our Interactive tcc shell, like this:

 $ ./itcc
 Released under GNU GPL version 2 or later, with NO WARRANTY.
 Type ".h" for help.
 
 tcc> int a = 5;
 tcc> a -= 2;
 tcc> if (a < 4) {
 [Compile error - type .e to see it.]
 tcc>    printf("a is %i\n", a);
 [Compile error - type .e to see it.]
 tcc> }
 a is 3
 tcc> |

Ignore errors. The result is printed after typing the closing brace "}".

Pass arguments to Interactive TCC and operate on them.

 $ ./itcc -- foo bar baz

 tcc> puts(argv[2]);
 bar
 tcc> |

Interactive Crap
================

Interactive, concise, regex-aware preprocessor (icrap) *is standard C* (using tcc in the background), without most of the semicolons, curly braces, and parenthesis. Like Python, use tab or indent 4 spaces instead of adding curly braces. Use two spaces instead of parenthesis. Since braces are added automatically, it saves typing. There are also some exciting, new go-like language features that really simplify C coding. Get crap from https://themanyone.github.io/crap/
 $ ./icrap -lm
 Released under GNU GPL version 2 or later, with NO WARRANTY.
 Type ".h" for help.

 crap> #include "math.h"
 crap> for  int x=0;x<5;x++
 crap>      printf  "%i squared is %0.0f\n", x, pow(x, 2.0)
 0 squared is 0
 1 squared is 1
 2 squared is 4
 3 squared is 9
 4 squared is 16
 crap> |

Supply includes and libs on the command line. Work with glib-2.0, plugins, etc. Test code without the compile step. Add extra CFLAGS and args. It's all free.

 icrap $(pkg-config --cflags --libs glib-2.0) -std=c99 -g -Wall -- foo myargs
 crap> .l
 #include <glib.h>
 #include <glib/gprintf.h>
 crap> GDateTime *dt=g_date_time_new_now_local ();
 crap> int yyyy,mm,dd
 crap> g_date_time_get_ymd dt, &yyyy, &mm, &dd
 crap> g_print "date: %.4d-%.2d-%.2d\n", yyyy, mm, dd
 date: 2024-02-14
 crap> puts  argv[2]
 myargs
 crap> |

Interactive Tcc and Interactive Crap build upon the original Interactive GCC (igcc), which is also included in this package. Those who have no problem converting C++ to C, might even be able to struggle through some of following examples using itcc, or icrap.

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
 g++>	cout << it->first << " " << it->second << endl;
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

The cstdio, iostream and string headers are automatically included, and the std namespace is already in scope.

Interactive Rust
================

We now run rust interactively. The first few arguments are passed along to the rust compiler. Everythig after the `--` is passed along to the interactive session, allowing programmers to play with them. As usual, ignore temporary compile errors until finishing closing brace. Get rust from http://rust-lang.org Command-line documentation https://rust-cli.github.io/book/tutorial/cli-args.html

 $ ./irust -- foo bar baz
 rustc 0.3
Released under GNU GPL version 2 or later, with NO WARRANTY.
Type ".h" for help.

 rust> use std::env;
 rust> let args: Vec<String> = env::args().collect();
 rust> for arg in args.iter() {
 [Compile error - type .e to see it.]
 rust> println!("{}", arg);
 [Compile error - type .e to see it.]
 rust> }
 foo
 bar
 baz
 rust> 

FAQ. Issues.
============

How does it work? Does it re-run the entire code block each time?

Yes. Although it runs all the code each time, it only prints the new output. Supposedly. There appears to be some bugs with detecting what was already printed, causing some new lines to produce no output. In that case, just press CTRL-C or CTRL-D and restart it. We're working on that...

Downloading and using
---------------------
itcc is published on GitHub. Get it from https://github.com/themanyone/itcc

Other REPLs
-----------
various languages in the browser http://repl.it
csharp: included with monodevelop http://www.csharphelp.com/
psysh: comes with php for php code http://php.net
evcxr: another Rust REPL https://github.com/evcxr/evcxr
ipython: interactive python https://github.com/ipython/ipython
rep.lua: a lua REPL https://github.com/hoelzro/lua-repl
re.pl: perl command line https://github.com/daurnimator/rep
d8-314: from V8, Javascript https://developers.google.com/v8/
csi: from chicken, a scheme REPL http://call-cc.org/
RStudio: interactive R coding https://rstudio.com/
Ruby IRB: REPL tool for Ruby https://ruby-doc.org/stdlib-2.7.2/libdoc/irb/rdoc/IRB.html
numerous bash-like shells and interpreters

Legacy Code
-----------

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

This fork is maintained with updated code, which is Copyright (C) 2024 by Henry Kroll III under the same license. Blame him if there are problems with these updates. Issues for this fork are maintained on GitHub.

Browse Themanyone
- GitHub https://github.com/themanyone
- YouTube https://www.youtube.com/themanyone
- Mastodon https://mastodon.social/@themanyone
- Linkedin https://www.linkedin.com/in/henry-kroll-iii-93860426/
- [TheNerdShow.com](http://thenerdshow.com/)
