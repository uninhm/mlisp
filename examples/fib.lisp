(def N 100)

(def (fib n)
  (def (iter a b c)
    (if (= c n)
      a
      (iter b (+ a b) (+ c 1))))
  (iter 0 1 0))

(print (fib N))