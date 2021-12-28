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
