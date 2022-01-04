(include "std.lisp")

(var fd:i64 (openat (- 100) "example_resources/aoc2021day1input" 0 440))

(def buf-size 9166) ; the file size plus 1
(var buf:ptr-char (reserve buf-size))
(read fd buf (- buf-size 1))
(close fd)

(var num-buf:ptr-char (reserve 10))
(var ans:i64 0)

(var n:i64)
(var a:i64 10000000000) ; just a very big number
(var b:i64 10000000000) ; TODO: make this INT_MAX or sth
(var c:i64 10000000000)

(var n:i64)
(var i:i64)
(while (!= (getp buf) 0)
  (if (= (getp buf) 10)
    (progn
      (setp (+ num-buf i) 0)
      (set n (parseint num-buf))
      (if (> n a)
        (set ans (+ ans 1)))
      (set a b)
      (set b c)
      (set c n)
      (set i 0))
    (progn
      (setp (+ num-buf i) (getp buf))
      (set i (+ i 1))))
  (set buf (+ buf 1)))

(print ans)
