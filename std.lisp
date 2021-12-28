(def SYS_read 0)
(def SYS_write 1)
(def STDIN 0)
(def STDOUT 1)
(def STDERR 2)

(def (puts s:ptr-char l:int)
  (syscall SYS_write STDOUT s l))

(def (input buf:ptr-char l:int)
  (syscall SYS_read STDIN buf l))

(def (!=:int a:int b:int) (not (= a b)))

(def (parseint-iter:int str:ptr-char i:int n:int)
  (if (= (getp (+ str i)) 0)
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

;; returns the length of the result
(def (repr:int buf-size:int buf:ptr-char n:int)
  (- buf-size (repr-iter buf (- buf-size 1) n)))

(def (strip-iter buf:ptr-char i:int)
  (if (= (getp (+ buf i)) 10)
    (setp (+ buf i) 0)
    (strip-iter buf (+ i 1))))

(def (strip buf:ptr-char)
  (strip-iter buf 0))
