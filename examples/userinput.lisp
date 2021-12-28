(include "std.lisp")

(def BUF_SIZE 32)

(def (parseint-iter:int str:ptr-char i:int n:int)
  (if (= (getp (+ str i)) 10)
    n
    (parseint-iter str
          (+ i 1)
          (+ (* n 10)
             (- (getp (+ str i)) ?0)))))

(def (parseint:int str:ptr-char)
  (parseint-iter str 0 0))

(def (repr-iter:int buf:ptr-char i:int n:int)
  (if (= n 0)
    i
    (progn
      (setp (+ buf i) (+ ?0 (% n 10)))
      (repr-iter buf
            (- i 1)
            (/ n 10)))))

(def (repr:int buf:ptr-char n:int)
  (repr-iter buf (- BUF_SIZE 1) n))

(reserve buf BUF_SIZE)
(reserve repr_buf BUF_SIZE)

(input buf BUF_SIZE)

(var i:int (repr repr_buf (+ 1 (parseint buf))))

(puts (+ repr_buf i) (- BUF_SIZE i))
(puts "\n" 1)
