# mlisp

A not-very-well-implemented compiler for a custom, lisp-inspired, typed language. See the examples to get an idea of how it works.

Disclaimer: This was my first take into compilers, I didn't do research on how to implement things. Don't expect it to follow x64 calling conventions or anything. In retrospective, it works shockingly well for what it is.

# Usage

If for some reason you want to try it, you have to be using Linux x64 and have nasm or fasm installed. Run this to get the help message:
```sh
$ python3 main.py
```
You can use `./run.sh <file>` script to compile, assemble and run a program.  
If you're using nasm you'll have to link manually. See `debug.sh`.
