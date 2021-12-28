(include "std.lisp")

(def (rec:int a:int b:int)
  (if (>= a 4000000)
      0
      (+ (rec b (+ a b))
         (* (even? a) a))))

(def buf-size 20)
(reserve buf buf-size)
(var repr-len:int
  (repr buf-size buf
        (rec 0 1)))
(puts (+ buf (- buf-size repr-len)) repr-len)
(puts "\n" 1)
