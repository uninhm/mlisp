(include "std.lisp")

(def BUF_SIZE 32)

(var buf:ptr-char (reserve BUF_SIZE))

(input buf BUF_SIZE)
(strip buf)

(print (+ 1 (parseint buf)))
