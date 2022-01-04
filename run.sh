#!/bin/sh
python main.py $1 && fasm out.asm > /dev/null && ./out
