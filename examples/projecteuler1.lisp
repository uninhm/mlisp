(include "std.lisp")

(def (loop:int i:int total:int)
  (if (= i 1000)
    total
    (if (= (% i 3) 0)
      (loop (+ i 1) (+ total i))
      (if (= (% i 5) 0)
        (loop (+ i 1) (+ total i))
        (loop (+ i 1) total)))))

(reserve repr-buf 20)
(var len:int
  (repr 20 repr-buf
    (loop 0 0)))
(puts (+ repr-buf (- 20 len)) len)
(puts "\n" 1)
