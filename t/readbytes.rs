use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::str;

fn main() {
    fn rdfile(file: &str) -> io::Result<()> {
        let f = File::open(file);
        let mut buffer = [0; 10];
        let n = f.expect("REASON").read(&mut buffer)?;
        println!("The bytes: {:?}", &buffer[..n]);
        Ok(())
    }
    let _ = rdfile("libigcc/version.py");
}
