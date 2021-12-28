(include "std.lisp")

(def (rec:int a:int b:int)
  (if (>= a 4000000)
      0
      (+ (rec b (+ a b))
         (* (even? a) a))))

(print (rec 0 1))
