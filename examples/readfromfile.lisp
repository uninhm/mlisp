(include "std.lisp")

(def buf-size 256)
(var buf:ptr-char (reserve buf-size))

(var fd:int (openat (- 100) "example_resources/readfromfile" 0 440))
(read fd buf buf-size)
(close fd)

(puts buf 5)
