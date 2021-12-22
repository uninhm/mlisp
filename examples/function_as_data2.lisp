(def (sq a) (* a a))
(def (double a) (+ a a))

(print
  ((if (> 2 3)
    sq
    double) 20))
