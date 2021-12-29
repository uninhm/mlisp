#!/bin/sh
python main.py -nasm $1 && nasm -felf64 -Fdwarf out.asm && ld -o out out.o && gdb ./out
