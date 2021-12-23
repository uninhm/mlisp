(def (parseint str)
  (def (iter i n)
    (if (= i (len str))
      n
      (iter (+ i 1)
            (+ (* n 10)
               (- (idx str i) ?0)))))
  (iter 0 0))

(print (+ 1 (parseint (input))))
