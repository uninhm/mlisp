(include "std.lisp")

(var dfd:int (openat (- 100) "example_resources" O_DIRECTORY 755))

(var fd:int (openat dfd "aoc2021day1input" O_RDONLY 440))

(def buf-size 9166) ; the file size plus 1
(var buf:ptr-char (reserve buf-size))
(read fd buf (- buf-size 1))
(close fd)
(close dfd)

(var num-buf:ptr-char (reserve 10))
(var ans:int 0)
(var last:int 10000000000) ; just a very big number
                           ; TODO: make this INT_MAX or sth

(var n:int)
(def (iter i:int)
  (if (!= (+ 0 (getp buf)) 0)
    (progn
      (if (= (getp buf) 10)
        (progn
          (setp (+ num-buf i) 0)
          (set n (parseint num-buf))
          (if (> n last)
            (set ans (+ ans 1)))
          (set last n)
          (set buf (+ buf 1))
          (iter 0))
        (progn
          (setp (+ num-buf i) (getp buf))
          (set buf (+ buf 1))
          (iter (+ i 1)))))))

(iter 0)
(print ans)
