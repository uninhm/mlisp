(def SYS_read 0)
(def SYS_write 1)
(def SYS_close 3)
(def SYS_openat 257)
(def STDIN 0)
(def STDOUT 1)
(def STDERR 2)

(def (openat:int dfd:int path:ptr-char flags:int mode:int)
  (syscall SYS_openat dfd path flags mode))

(def (read fd:int buf:ptr-char count:int)
  (syscall SYS_read fd buf count))

(def (write fd:int buf:ptr-char count:int)
  (syscall SYS_write fd buf count))

(def (close fd:int)
  (syscall SYS_close fd))

(def (puts s:ptr-char count:int)
  (write STDOUT s count))

(def (input buf:ptr-char count:int)
  (read STDIN buf count))

(def (!=:int a:int b:int) (not (= a b)))
(def (>=:int a:int b:int) (not (< a b)))
(def (>:int a:int b:int) (& (>= a b) (!= a b)))
(def (<=:int a:int b:int) (not (> a b)))

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
  (- (- buf-size 1) (repr-iter buf (- buf-size 1) n)))

(def (strip-iter buf:ptr-char i:int)
  (if (= (getp (+ buf i)) 10)
    (setp (+ buf i) 0)
    (strip-iter buf (+ i 1))))

(def (strip buf:ptr-char)
  (strip-iter buf 0))

(def (even?:int n:int) (= (% n 2) 0))

(def (print n:int)
  (def buf-size 20)
  (var buf:ptr-char (reserve buf-size)) ; TODO use stack instead
  (var repr-len:int
    (repr buf-size buf n))
  (puts (+ buf (- buf-size repr-len)) repr-len)
  (puts "\n" 1))
