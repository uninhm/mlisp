(def SYS_read 0)
(def SYS_write 1)
(def SYS_close 3)
(def SYS_openat 257)
(def STDIN 0)
(def STDOUT 1)
(def STDERR 2)

(def O_RDONLY 0)
(def O_WRONLY 1)
(def O_RDWR 2)
(def O_CREAT 64)
(def O_TRUNC 512)
(def O_APPEND 1024)
(def O_DIRECTORY 65536)

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

(def (>=:int a:int b:int) (not (< a b)))
(def (>:int a:int b:int) (& (>= a b) (!= a b)))
(def (<=:int a:int b:int) (not (> a b)))

(def (parseint:int str:ptr-char)
  (var n:int 0)
  (while (!= (getp str) 0)
    (set n (+ (* n 10)
              (- (getp str) ?0)))
    (set str (+ str 1)))
  n)

;; returns the length of the result
(def (repr:int buf-size:int buf:ptr-char n:int)
  (var i:int 1)
  (while (!= n 0)
    (setp (+ buf (- buf-size i)) (+ ?0 (% n 10)))
    (set n (/ n 10))
    (set i (+ i 1)))
  (- i 1))

(def (strip buf:ptr-char)
  (while (!= (getp buf) 10)
    (set buf (+ buf 1)))
  (setp buf 0))

(def (even?:int n:int) (= (% n 2) 0))

(def (print n:int)
  (def buf-size 20)
  (var buf:ptr-char (reserve buf-size)) ; TODO use stack instead
  (var repr-len:int
    (repr buf-size buf n))
  (puts (+ buf (- buf-size repr-len)) repr-len)
  (puts "\n" 1))
