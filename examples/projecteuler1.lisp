(include "std.lisp")

(def (loop:int i:int total:int)
  (if (= i 1000)
    total
    (if (= (% i 3) 0)
      (loop (+ i 1) (+ total i))
      (if (= (% i 5) 0)
        (loop (+ i 1) (+ total i))
        (loop (+ i 1) total)))))

(print (loop 0 0))
