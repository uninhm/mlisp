(include "std.lisp")

(def buf-size 256)
(reserve buf buf-size)

(var fd:int (openat (- 100) "testfile.txt" 0 440))
(read fd buf buf-size)

(puts buf buf-size)
