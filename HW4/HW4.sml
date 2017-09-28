(* Alexander Lao *);
(* 11481444 *);
(* CptS 355 - Assignment 4 (Standard ML) *);

(* 1. filter and reverse ................. line 23 *);
(* 2. subsets ............................ line 63 *);
(* 3. pairNleft and pairNright ........... line 79 *);
(* 4. exists ............................. line 38 *);
(* 5. listUnion .......................... line 49 *);
(* 6. listDiff ........................... line 118 *);
(* 7. merge sort ......................... line 131 *);
(* 8. practice with datatypes ............ line 160 *);
(* test cases ............................ line 196 *);

(* the fold function we defined in lecture *);
fun fold f base [] = base
  | fold f base (x::rest) = f x (fold f base rest);

(* the map function we defined in lecture *);
fun map f [] = []
  | map f (x::rest) = (f x)::(map f rest);

(* ============================ 1. filter and reverse ============================ *);

(* tail recursive auxillary function to help the filter function *);
(* the result is in reversed order *);
fun accum pred acc [] = acc
  | accum pred acc (x::rest) = if pred x then accum pred (x::acc) rest
							   else accum pred acc rest;

(* tail recursive function to reverse a list *);
fun reverse ([], L) = L
  | reverse (x::rest, L) = reverse (rest, x::L);

(* filter function that reverses the output of the auxillary function *);
fun filter pred L = reverse (accum pred [] L, []);

(* ============================ 4. exists ============================ *);

(* exists needs to be declared before listUnion because listUnion calls exists *);

(* checks if a value n exists in the list L *);
(* the type is (''a * ''a list) -> bool and not ('a * 'a list) -> bool
   because the types need to be supported in equality testing *);
fun exists (n, []) = false
  | exists (n, x::rest) = if x = n then true
						  else exists (n, rest);

(* ============================ 5. listUnion ============================ *);

(* listUnion needs to be declared before subsets because subsets calls listUnion *);

(* auxillary function to help the list union function *);
(* uses the exists function to check if an item from one list exists in the other list *);
fun doUnion ([], L2) = L2
  | doUnion (x::rest, L2) = if exists (x, L2) then doUnion (rest, L2)
							else doUnion (rest, x::L2);

(* the listUnion function calls the doUnion function twice to eliminate duplicates in L2 *);
(* the result will not be in order *);
fun listUnion (L1, L2) = doUnion (L1, doUnion (L2, []));

(* ============================ 2. subsets ============================ *);

(* helper function for the subsets function *);
(* will cons a value x to every item in a list of lists *);
(* expects a list of lists to be passed in *);
fun doSubsets x [] = []
  | doSubsets x (y::rest) = (x::y)::(doSubsets x rest);

(* creates a list of lists given a list *);
(* each sublist will be a subset of the given list *);
(* calls on the listUnion function to combine lists *);
(* when the doSubsets function is called, we need to call subsets on rest
   in order to create a list of lists because doSubsets expects a list of lists *);
fun subsets [] = [[]]
  | subsets (x::rest) = listUnion ((doSubsets x (subsets rest)), (subsets rest));

(* ============================ 3. pairNleft and pairNright ============================ *);

(* returns the length of a list *);
fun length [] = 0
  | length (x::rest) = 1 + length rest;

(* auxillary function for pairNright *);
(* if the acc is less than the n value, cons to the same acc *);
(* otherwise make a new acc with the x value and recursively call the auxRight on the new acc *);
(* need to reverse the old acc because items are appended from left to right *);
fun auxRight n [] acc = [acc]
  | auxRight n (x::rest) acc = if (length acc) < n then auxRight n rest (x::acc)
							   else (reverse (acc, []))::(auxRight n rest (x::[]));

(* auxillary function for pairNleft *);
(* same idea as pairNright except we don't need to reverse the old acc because
   we passed in the reverse of the original list *);
fun auxLeft n [] acc = [acc]
  | auxLeft n (x::rest) acc = if (length acc) < n then auxLeft n rest (x::acc)
							  else acc::(auxLeft n rest (x::[]));

(* reverses the last sublist in a list of lists *);
fun revLast [] = []
  | revLast (x::rest) = if rest = [] then [reverse (x, [])]
						else x::(revLast rest);

(* calls the auxRight function to do all the work *);
(* calls the revLast function because in the auxRight function,
   we only reverse the acc if we fill up the sublist (i.e. the acc's
   length is >= the n value). therefore, the furthest right sublist would be in
   reversed order if we finished the function before the last sublist could
   reach a value greater than or equal to the n value *);
fun pairNright n L = revLast (auxRight n L []);

(* calls the auxLeft function to do all the work *);
(* reverses the original list L so we don't need to reverse the old acc *);
(* reverses the entire result because the auxLeft will return a reversed list list *);
fun pairNleft n L = reverse ((auxLeft n (reverse (L, [])) []), []);

(* ============================ 6. listDiff ============================ *);

(* removes the first occurrence of value n from a list L *);
fun remove n [] = []
  | remove n (x::rest) = if n = x then rest
						 else x::remove n rest;

(* returns the difference of two lists *);
(* if an item in L2 exists in L1, remove it from L1 *);
fun listDiff L1 [] = L1
  | listDiff L1 (x::rest) = if exists (x, L1) then listDiff (remove x L1) rest
						    else listDiff L1 rest;

(* ============================ 7. merge sort ============================ *);

(* separates each item in a list into its own sublist *)
(* returns a list of lists *);
fun unitLists ([]) = []
  | unitLists ((x::rest)) = (x::[])::(unitLists (rest));

(* merges two sorted lists in sorted order. same algorithm as the scheme assignment's merge2 *);
fun merge2 [] L2 = L2
  | merge2 L1 [] = L1
  | merge2 (x::restX) (y::restY) = if x < y then (x::(merge2 restX (y::restY)))
								   else (y::(merge2 restY (x::restX)));

(* auxillary function for mergeSort *);
(* accepts a list of lists and calls merge2 on the sublists *);
fun mergeAux [] = []
  | mergeAux [x] = x
  | mergeAux (x::y::rest) = mergeAux ((merge2 x y)::rest);

(* function call for mergeSort which retains duplicates *);
(* calls unitLists on the list L first to create a list of lists of single elements *);
fun mergeSort L = mergeAux (unitLists L);

(* function call for mergeSort2 which removes duplicates *);
(* calls listUnion on itself to remove duplicates of the orignal list L*);
(* then reverses the list with no duplicates because listUnion returns a backwards list *);
(* then calls unitLists on the list L to create a list of lists of single elements *);
fun mergeSort2 L = mergeAux (unitLists (reverse ((listUnion (L, L)), [])));

(* ============================ 8. practice with datatypes ============================ *);

(* user defined datatype for values of strings or ints *);
datatype either = ImAString of string | ImAnInt of int;

(* user defined datatype for a binary tree *);
datatype eitherTree = INTERIOR of (eitherTree * either * eitherTree) | LEAF of either;

(* searches a binary tree for an int v *);
(* checks all cases: if it's a leaf of type int, leaf of type string,
   internal of type int, or internal of type string *);
fun eitherSearch (LEAF (ImAnInt (x))) v = if x = v then true else false
  | eitherSearch (LEAF (ImAString (x))) v = false
  | eitherSearch (INTERIOR (c1, (ImAnInt (x)), c2)) v = if x = v then true
													    else eitherSearch (c1) v orelse eitherSearch (c2) v
  | eitherSearch (INTERIOR (c1, (ImAString (x)), c2)) v = eitherSearch (c1) v orelse eitherSearch (c2) v;

(* creating a tree *);
val L1 = LEAF (ImAnInt 1);
val L2 = LEAF (ImAnInt 2);
val L3 = LEAF (ImAnInt 3);
val L4 = LEAF (ImAnInt 4);
val L5 = LEAF (ImAnInt 5);
val L6 = LEAF (ImAnInt 6);
val L7 = LEAF (ImAString "a");

val T4 = INTERIOR (L1, ImAString "g", L2);
val T1 = INTERIOR (T4, ImAnInt 8, L7);
val T6 = INTERIOR (L3, ImAString "i", L5);
val T5 = INTERIOR (T6, ImAString "h", L4);
val T3 = INTERIOR (L6, ImAnInt 10, T5);
val ROOT = INTERIOR (T1, ImAnInt 9, T3);

(* tests the eitherSearch function *);
fun eitherTest T v = eitherSearch T v;

(* ==================== TEST FUNCTIONS ==================== *);

fun testFilter (pred, L, R) = if (filter pred L) = R then true else false;
val testFilterOne = testFilter ((fn (x) => (x = 1)), [1, 2, 3], [1]);
val testFilterTwo = testFilter ((fn (x) => (x > 1)), [1, 2, 3, 4, 5, 6], [2, 3, 4, 5, 6]);
val testFilterThree = testFilter ((fn (x) => (x = 0)), [1, 2, 3, 4, 5, 6], []);

fun testSubsets (L, R) = if (subsets L) = R then true else false;
val testSubsetsOne = testSubsets ([1, 2, 3], [[1, 3], [1], [1, 2, 3], [1, 2], [3], [], [2, 3], [2]]);
val testSubsetsTwo = testSubsets ([], [[]]);
val testSubsetsThree = testSubsets ([4, 5], [[4], [4, 5], [], [5]]);

fun testPairNLeft (n, L, R) = if (pairNleft n L) = R then true else false;
val testPairNLeftOne = testPairNLeft (2, [1, 2, 3, 4, 5], [[1], [2, 3], [4, 5]]);
val testPairNLeftTwo = testPairNLeft (3, [1, 2, 3, 4, 5], [[1, 2], [3, 4, 5]]);
val testPairNLeftThree = testPairNLeft (5, [1, 2, 3, 4, 5], [[1, 2, 3, 4, 5]]);

fun testPairNRight (n, L, R) = if (pairNright n L) = R then true else false;
val testPairNRightOne = testPairNRight (2, [1, 2, 3, 4, 5], [[1, 2], [3, 4], [5]]);
val testPairNRightTwo = testPairNRight (3, [1, 2, 3, 4, 5], [[1, 2, 3], [4, 5]]);
val testPairNRightThree = testPairNRight (5, [1, 2, 3, 4, 5], [[1, 2, 3, 4, 5]]);

fun testExists (n, L, R) = if (exists (n, L)) = R then true else false;
val testExistsOne = testExists (1, [1, 2, 3], true);
val testExistsTwo = testExists (4, [1, 2, 3], false);
val testExistsThree = testExists ("hello", ["hey", "hi", "hello"], true);
val testExistsFour = testExists ([1, 4, 5], [[1, 2, 3], [4, 6, 8], [1, 4, 5], [4, 5, 1]], true);

fun testListUnion (L1, L2, R) = if (listUnion (L1, L2)) = R then true else false;
val testListUnionOne = testListUnion ([1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1]);
val testListUnionTwo = testListUnion ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7], [7, 6, 5, 4, 3, 2, 1]);
val testListUnionThree = testListUnion ([[1, 1], [2, 1]], [[1], [1], [1], [1, 1]], [[2, 1], [1, 1], [1]]);
val testListUnionFour = testListUnion ([], [], []);

fun testListDiff (L1, L2, R) = if (listDiff L1 L2) = R then true else false;
val testListDiffOne = testListDiff ([1, 2, 3], [1, 2, 3], []);
val testListDiffTwo = testListDiff ([1, 2, 3], [1, 2, 3, 4, 5], []);
val testListDiffThree = testListDiff ([1, 1, 2, 3], [1, 2, 3], [1]);
val testListDiffFour = testListDiff ([1, 2, 3, 3, 3, 3, 4], [1, 2, 3, 3, 3], [3, 4]);
val testListDiffFive = testListDiff ([], [1, 2, 3], []);
val testListDiffSix = testListDiff ([1, 5], [1, 1, 1, 1, 1, 2, 3], [5]);

fun testUnitLists (L, R) = if (unitLists (L)) = R then true else false;
val testUnitListsOne = testUnitLists ([1, 2, 3, 4, 5], [[1], [2], [3], [4], [5]]);
val testUnitListsTwo = testUnitLists ([], []);
val testUnitListsThree = testUnitLists ([5000, 2000, 1000], [[5000], [2000], [1000]]);

fun testMergeSort (L, R) = if (mergeSort L) = R then true else false;
val testMergeSortOne = testMergeSort ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]);
val testMergeSortTwo = testMergeSort ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]);
val testMergeSortThree = testMergeSort ([1, 1, 1, 3, 3, 3, 2, 1, 3], [1, 1, 1, 1, 2, 3, 3, 3, 3]);

fun testMergeSort2 (L, R) = if (mergeSort2 L) = R then true else false;
val testMergeSort2One = testMergeSort2 ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]);
val testMergeSort2Two = testMergeSort2 ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]);
val testMergeSort2Three = testMergeSort2 ([1, 1, 3, 4, 2, 1, 4, 1, 2, 3, 3, 4, 1, 1, 4, 2], [1, 2, 3, 4]);
val testMergeSort2Four = testMergeSort2 ([], []);

val eitherTestShouldBeTrue = eitherTest ROOT 5;
val eitherTestShouldBeFalse = eitherTest ROOT 1000;