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

(def (openat:i64 dfd:i64 path:ptr-char flags:i64 mode:i64)
  (syscall SYS_openat dfd path flags mode))

(def (read fd:i64 buf:ptr-char count:i64)
  (syscall SYS_read fd buf count))

(def (write fd:i64 buf:ptr-char count:i64)
  (syscall SYS_write fd buf count))

(def (close fd:i64)
  (syscall SYS_close fd))

(def (puts s:ptr-char count:i64)
  (write STDOUT s count))

(def (input buf:ptr-char count:i64)
  (read STDIN buf count))

(def (>=:i64 a:i64 b:i64) (not (< a b)))
(def (>:i64 a:i64 b:i64) (& (>= a b) (!= a b)))
(def (<=:i64 a:i64 b:i64) (not (> a b)))

(def (parseint:i64 str:ptr-char)
  (var n:i64 0)
  (while (!= (getp str) 0)
    (set n (+ (* n 10)
              (- (getp str) ?0)))
    (set str (+ str 1)))
  n)

;; returns the length of the result
(def (repr:i64 buf-size:i64 buf:ptr-char n:i64)
  (var i:i64 1)
  (while (!= n 0)
    (setp (+ buf (- buf-size i)) (+ ?0 (% n 10)))
    (set n (/ n 10))
    (set i (+ i 1)))
  (- i 1))

(def (strip buf:ptr-char)
  (while (!= (getp buf) 10)
    (set buf (+ buf 1)))
  (setp buf 0))

(def (even?:i64 n:i64) (= (% n 2) 0))

(def (print n:i64)
  (def buf-size 20)
  (var buf:ptr-char (reserve buf-size)) ; TODO use stack instead
  (var repr-len:i64
    (repr buf-size buf n))
  (puts (+ buf (- buf-size repr-len)) repr-len)
  (puts "\n" 1))
