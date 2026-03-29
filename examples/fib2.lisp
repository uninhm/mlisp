(include "std.lisp")

(def (fib:int n:int)
  (def (go:int n:int a:int b:int)
    (if (= n 0)
      a
      (go (- n 1) b (+ a b))))
  (go n 0 1))

(print (fib 20))
