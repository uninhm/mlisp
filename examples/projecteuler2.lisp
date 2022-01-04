(include "std.lisp")

(def (rec:i64 a:i64 b:i64)
  (if (>= a 4000000)
      0
      (+ (rec b (+ a b))
         (* (even? a) a))))

(print (rec 0 1))
