(include "std.lisp")

(var total:i64 0)
(var i:i64 0)

(while (< i 1000)
  (if (| (= (% i 3) 0) (= (% i 5) 0))
    (set total (+ total i)))
  (set i (+ i 1)))

(print total)
