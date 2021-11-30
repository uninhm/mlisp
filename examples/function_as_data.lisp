(def (square x) (* x x))
(def (double x) (+ x x))

(def (f x)
  ((if (< x 10)
       square
       double)
   x))

(print (f 5))
(print (f 20))