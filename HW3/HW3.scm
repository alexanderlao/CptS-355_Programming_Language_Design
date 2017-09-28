; Alexander Lao
; 11481444
; CPTS355 - ASSIGNMENT 3 (SCHEME)

; counts items in a list including sublists
; if an item is a sublist, it will recursively go through the sublist
; otherwise just add one to the counter
(define (deepCount L) (cond
                        ((null? L) 0)
                        ((pair? (car L)) (+ (deepCount (car L)) (deepCount (cdr L))))
                        (else (+ 1 (deepCount (cdr L))))
                        )
  )

; returns the nth item of a list
; the function will iterate through the list
; by recursively calling the decrement of n and the cdr of L
; once n is equal to zero, it means we're at the correct index
; otherwise return an empty list meaning the index is not found
(define (nthElement n L) (cond
                           ((null? L) '())
                           ((eq? n 0) (car L))
                           (else (nthElement (- n 1) (cdr L)))
                           )
  )

; replaces the nth item in the list with value v
; the function will iterate through the list
; looking for the correct index by recursively calling the
; decrement of n and the cdr of L
; once n is equal to zero, it means we're at the correct index
; so cons the value with the cdr of L
; otherwise keep the list the same and make the next recursive call
(define (repL n v L) (cond
                       ((null? L) '())
                       ((eq? n 0) (cons v (cdr L)))
                       (else (cons (car L) (repL (- n 1) v (cdr L))))
                       )
  )

; returns a list of values starting with min, adding step to min each time, and
; ending before it hits the value max
; if the min >= max and step >= 0, return an empty list (counting up)
; if the min <= max and step < 0, return an empty list (counting down)
(define (range min step max) (cond
                               ((and (>= min max) (>= step 0)) '())
                               ((and (<= min max) (< step 0)) '())
                               (else (cons min (range (+ min step) step max)))
                               )
  )

; merges two lists L1 and L2 in ascending order
; pre-condition: lists are already in ascending order
; if one list is empty, return the other because it's already in sorted order
; if the car of L1 is less than the car of L2, cons the car of L1 and make
; the recursive call to the cdr of L1 and the full list of L2
; vice versa if the car of L2 is less than the car of L1
(define (merge2 L1 L2) (cond
                         ((null? L1) L2)
                         ((null? L2) L1)
                         ((< (car L1) (car L2)) (cons (car L1) (merge2 (cdr L1) L2)))
                         (else (cons (car L2) (merge2 (cdr L2) L1)))
                         )
  )
  
; the fold function we defined in lecture
(define (fold f base L) (cond
                          ((null? L) base)
                          (else (f (car L) (fold f base (cdr L))))
                          )
  )

; sorts a list of sorted sublists in ascending order
; makes use of the fold function which uses merge2 in
; an anonymous function
; it is difficult to generalize the amount of times cons is called
; due to the nature of the lists. if we look at the function merge2 on
; lists L1 = (1 2) and L2 = (3 4), we see cons is only called twice because
; L1 goes to null and we just append the entire L2.
; for lists L1 = (2 3) and L2 = (1 4), cons is called three times because
; cons will be called back and forth between L1 and L2 (one list won't go
; to null before the other list can reach only one element)
; so for my implementation, in the worst case scenario merge2 is
; calling cons (len1 + len2 - 1) times
; for the mergeN function, the worst case scenario will
; call cons n(len1 + len2 + ... + lenN) times where n is the number of
; sublists and len1, len2, ..., lenN are the lengths of sublist1, sublist2,
; ..., and sublistN respectively.
(define (mergeN Ln) (fold (lambda (x y) (merge2 x y)) '() Ln))

; the mymap function we defined in lecture
; has an additional check for pairs (sublists)
(define (mymap f L) (cond
                     ((null? L) '())
                     ((pair? (car L)) (cons (mymap f (car L)) (mymap f (cdr L))))
                     (else (cons (f (car L)) (mymap f (cdr L))))
                     )
  )

; applies a passed in function as a parameter to a matrix
; makes use of the mymap function which includes an
; additional check for pairs (sublists)
(define (matrixMap f M) (mymap f M))

; the filter function we defined in lecture
(define (filter pred L) (cond
                          ((null? L) '())
                          ((pred (car L)) (cons (car L) (filter pred (cdr L))))
                          (else (filter pred (cdr L)))
                          )
  )

; adds up the numbers in a list
; helper function for avgOdd
; utilizes fold
(define (addUp L) (fold + 0 L))

; calculates the average of the odd numbers in a list
; uses the filter function to filter out numbers that are even
; calls the addUp function to determine to sum of the odd list
; calls the deepCount function to determine the length of the odd list
; divides the two to calculate the average
; if the odd list has a length of zero (a list of all even numbers or an empty list
; was passed in), return zero
(define (avgOdd L) (cond
                     ((eq? (deepCount (filter odd? L)) 0) 0)
                     (else (/ (addup (filter odd? L)) (deepCount (filter odd? L))))
                     )
  )

; ****************************** TEST FUNCTIONS ******************************

; rL is the expected result
(define (testDeepCount L rL) (cond
                               ((eq? (deepCount L) rL) #t)
                               (else #f)
                               )
  )

; must use equal? to compare lists
(define (testNthElement n L rL) (cond
                                  ((equal? (nthElement n L) rL) #t)
                                  (else #f)
                                  )
  )

(define (testRepL n v L rL) (cond
                              ((equal? (repL n v L) rL) #t)
                              (else #f)
                              )
  )

(define (testRange min step max rL) (cond
                                      ((equal? (range min step max) rL) #t)
                                      (else #f)
                                      )
  )

(define (testMerge2 L1 L2 rL) (cond
                                ((equal? (merge2 L1 L2) rL) #t)
                                (else #f)
                                )
  )

(define (testMergeN Ln rL) (cond
                             ((equal? (mergeN Ln) rL) #t)
                             (else #f)
                             )
  )

(define (testMatrixMap f M rM) (cond
                                 ((equal? (matrixMap f M) rM) #t)
                                 (else #f)
                                 )
  )

(define (testAvgOdd L r) (cond
                           ((eq? (avgOdd L) r) #t)
                           (else #f)
                           )
  )

; calls every test function
; each conditional will compare the output of the test function to false
; if a test function returns false (failed), the conditional will compare false to false and return false
; if a test function returns true (passed), the conditional will compare true to false and do nothing
(define (testAll) (cond
                    ((equal? (testDeepCount '(1 (2 3) 4 "5" (6)) 6) #f) #f)
                    ((equal? (testDeepCount '() 0) #f) #f)
                    ((equal? (testNthElement 0 '((1) 2 "3" (4 5)) '(1)) #f) #f)
                    ((equal? (testNthElement 1 '((1) 2 "3" (4 5)) 2) #f) #f)
                    ((equal? (testNthElement 2 '((1) 2 "3" (4 5)) "3") #f) #f)
                    ((equal? (testNthElement 3 '((1) 2 "3" (4 5)) '(4 5)) #f) #f)
                    ((equal? (testRepL 0 "Hello World!" '((1) 2 "3" (4 5)) '("Hello World!" 2 "3" (4 5))) #f) #f)
                    ((equal? (testRepL 1 '() '((1) 2 "3" (4 5)) '((1) () "3" (4 5))) #f) #f)
                    ((equal? (testRepL 2 100 '((1) 2 "3" (4 5)) '((1) 2 100 (4 5))) #f) #f)
                    ((equal? (testRepL 3 '(1 2 3 4) '((1) 2 "3" (4 5)) '((1) 2 "3" (1 2 3 4))) #f) #f)
                    ((equal? (testRange 0 5 34 '(0 5 10 15 20 25 30)) #f) #f)
                    ((equal? (testRange 10 -5 0 '(10 5)) #f) #f)
                    ((equal? (testRange 100 -100 0 '(100)) #f) #f)
                    ((equal? (testMerge2 '(1 3 4) '(1 3 4) '(1 1 3 3 4 4)) #f) #f)
                    ((equal? (testMerge2 '(1) '(1 3 4) '(1 1 3 4)) #f) #f)
                    ((equal? (testMerge2 '(1 2 100) '(1 2) '(1 1 2 2 100)) #f) #f)
                    ((equal? (testMerge2 '() '(1 2 3 4 5) '(1 2 3 4 5)) #f) #f)
                    ((equal? (testMerge2 '(100) '() '(100)) #f) #f)
                    ((equal? (testMerge2 '() '() '()) #f) #f)
                    ((equal? (testMergeN '() '()) #f) #f)
                    ((equal? (testMergeN '((10 20 30) (5 15 25)) '(5 10 15 20 25 30)) #f) #f)
                    ((equal? (testMergeN '((1 1 1 1) (1 1 1 1 1) (1) (1 1)) '(1 1 1 1 1 1 1 1 1 1 1 1)) #f) #f)
                    ((equal? (testMergeN '((15 16 17) (12 13 14) (9 10 11)) '(9 10 11 12 13 14 15 16 17)) #f) #f)
                    ; squaring each element
                    ((equal? (testMatrixMap (lambda (x) (* x x)) '((2 3) (4 5)) '((4 9) (16 25))) #f) #f)
                    ; subtracting one from each element
                    ((equal? (testMatrixMap (lambda (x) (- x 1)) '((2 3) (4 5)) '((1 2) (3 4))) #f) #f)
                    ; dividing each element by one
                    ((equal? (testMatrixMap (lambda (x) (/ x 1)) '((2 3)(100 200)) '((2 3)(100 200))) #f) #f)
                    ((equal? (testAvgOdd '(1 3 5) 3) #f) #f)
                    ((equal? (testAvgOdd '(2 4 6) 0) #f) #f)
                    ((equal? (testAvgOdd '() 0) #f) #f)
                    ((equal? (testAvgOdd '(1 2 3 4 5 6 7 8 9 10) 5) #f) #f)
                    (else (display "All tests passed!"))
                    )
  )

; call the testAll function
(testAll)