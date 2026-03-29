(include "std.lisp")

(def (fib:int n:int)
  (if (< n 2)
    n
    (+ (fib (- n 1)) (fib (- n 2)))))

(print (fib 20))
