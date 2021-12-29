#!/bin/sh
python main.py $@ && fasm out.asm > /dev/null && ./out
