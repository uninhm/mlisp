(def (f n s)
    (if (= n 0)
        s
        (f (- n 1)
           (+ s
              (if (or (= 0 (mod n 5)) (= 0 (mod n 3)))
                  n
                  0)))))
(f 999 0)