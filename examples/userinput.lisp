(include "std.lisp")

(def BUF_SIZE 32)

(reserve buf BUF_SIZE)
(reserve repr-buf BUF_SIZE)

(input buf BUF_SIZE)
(strip buf)

(var repr-len:int
  (repr BUF_SIZE repr-buf (+ 1 (parseint buf))))

(puts (+ repr-buf (- BUF_SIZE repr-len)) repr-len)
(puts "\n" 1)
