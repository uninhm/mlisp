#!/bin/sh
python main.py $1 && nasm -felf64 -Fdwarf out.asm && ld -o out out.o && gdb ./out
