// main.ha
use fmt;
use test;
use types::c;

@symbol("hello") fn c_hello() void;

export fn main() void = {
	test::print(test::hello);
	c_hello();
};
