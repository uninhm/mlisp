(include "std.lisp")

(def BUF_SIZE 32)

(reserve buf BUF_SIZE)
(reserve repr-buf BUF_SIZE)

(input buf BUF_SIZE)
(strip buf)

(print (+ 1 (parseint buf)))
