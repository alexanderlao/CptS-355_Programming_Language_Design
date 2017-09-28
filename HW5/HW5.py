# Alexander Lao
# Intended for Windows

# PART ONE: Lines 25 - 176
# PART TWO: Lines 179 - 296
# TEST CODE: Lines 300 - 582
# HW5 TEST CODE: Lines 498 - 582
# MAIN: Line 614

# WHAT CHANGED FOR HW5: The lookup () function: line 48, the stack () function: line 148,
#                       and the def () function: line 163 have all been modified. The dict (),
#                       begin (), and end () functions have been removed as well as their test cases.

# NOTE: When a function is called, its name is being pushed to the operand stack.
#       It's being pushed on line 288, but it should be going into the
#       if-statement on line 284 and skipping the else-statement.
#
#       Also, the order of the operand stack is different everytime the program is ran.
#       I do not know why this is happening, but it shouldn't affect the output.

# counter to keep track of the static links
staticCount = 0

# The operand stack: define the operand stack and its operations
opstack = []

# the hot end of the stack will
# be at the end of the list (n - 1)
def opPop (): 
    return opstack.pop ()               # remove the last item in the list

def opPush (value):
    opstack.append (value)              # append the value to the end of the list

# The dictionary stack: define the dictionary stack and its operations
dictstack = []

def dictPop ():
    return dictstack.pop ()             # remove the last dict in the list

def dictPush (newDict):
    dictstack.append (newDict)          # add the new dictionary to the dictionary stack

def define (name, value):
    name = {name : value}               # store the dict entry in name
    return name

def lookup (name, rule):                                        # lookup the name based on static or dynamic scoping
    if rule == "static":                                        # search for variable/function based on the static links
        for t in (dictstack):                                   # look at each tuple in the dictstack
            if name in t[1]:                                    # search for the name in the tuple's dict
                if isinstance (t[1][name], list):               # if the name is associated with a code array (calling a function)
                    global staticCount                          # referencing the global variable
                    staticCount = dictstack.index (t)           # set the static link to the function's definition's dict index
                    dictstack.append ((staticCount, {}))        # append an empty dictionary with the static link
                    interpret (t[1][name], rule)                # call that function
                    dictPop ()                                  # pop the dict after we're done calling the function
                else: return t[1][name]                         # check if the staticCount matches the correct activation record
            else: pass                                          # if the name is not in the dictstack, do nothing
    elif rule == "dynamic":                                     # search for variable/function from the top of the stack down
        for t in reversed (dictstack):                          # look at each tuple in the reversed dictstack
            if name in t[1]:                                    # search for the name in the tuple's dict
                if isinstance (t[1][name], list):               # if the name is associated with a code array
                    staticCount = t[0]                          # set the static link to the function's definition's dict index
                    dictstack.append ((staticCount, {}))        # append an empty dictionary
                    interpret (t[1][name], rule)                # call that function
                    dictPop ()                                  # pop the dict after we're done calling the function
                else: return t[1][name]                         # otherwise just return the value associated with the name
            else: pass                                          # if the name is not in the dictstack, do nothing

# Arithmetic operators: define all the arithmetic operators here -- add, sub, mul, div, mod
def opAdd ():
    v = opPop () + opPop ()             # pop the top two items on the stack and add them together
    opPush (v)                          # push the sum onto the stack

def opSub ():
    v =  opPop () - opPop ()            # pop the top two items on the stack and subtract them
    opPush (v)                          # push the difference onto the stack

def opMul ():
    v = opPop () * opPop ()             # pop the top two items on the stack and multiply them
    opPush (v)                          # push the product onto the stack

def opDiv ():
    v = opPop () / opPop ()             # pop the top two items on the stack and divide them
    opPush (v)                          # push the quotient onto the stack

def opMod ():
    v = opPop () % opPop ()             # pop the top two items on the stack and mod them
    opPush (v)                          # push the result onto the stack

# String operators: define all the string operators -- length, get, put, getinterval
def opLength ():
    string = opPop ()                   # pop the string off the stack
    string = string[1:-1]               # parse the string to get rid of the parenthesis
    length = 0                          # define a local counter to hold the length                            
    for x in string:                    # for every character in the string
        length += 1                     # add 1 to the length
    opPush (length)                     # push the length onto the stack

def opGet ():
    index = opPop ()                    # pop the index off the stack
    string = opPop ()                   # pop the string off the stack
    string = string[1:-1]               # parse the string to get rid of the parenthesis
    a = ord (string[index])             # convert the character at the string's index to its ascii value
    opPush (a)                          # push the ascii value onto the stack

def opPut ():
    value = opPop ()                    # pop the ascii value off the stack
    index = opPop ()                    # pop the index off the stack
    string = opPop ()                   # pop the string off the stack
    string = string[1:-1]               # parse the string to get rid of the parenthesis
    char = chr (value)                  # convert the ascii value to a character
    string = string[:index] + char + string[index + 1:]       # replacing the specified index in the string with the new character
    opPush (string)
    
def opGetInterval ():
    count = opPop ()                    # pop the count off the stack
    index = opPop ()                    # pop the index off the stack
    string = opPop ()                   # pop the string off the stack
    string = string[1:-1]               # parse the string to get rid of the parenthesis
    substr = string[index:count]        # get the substring based on the index and count
    opPush (substr)                     # push the substring onto the stack

# Define the stack manipulation and print operators: dup, exch, pop, roll, copy, clear, stack
def opDup ():
    value = opstack[-1]                 # store the last item in the opstack in a local variable
    opPush (value)                      # push the last item onto the stack

def opExch ():
    first = opPop ()                    # pop the last item off stack
    second = opPop ()                   # pop the next item off the stack
    opPush (first)                      # push the first value we popped onto the stack
    opPush (second)                     # push the second value we popped onto the stack

def opPopRemove ():
    opstack.pop ()                      # pop the last item off the stack

def opRoll ():
    number = opPop ()                   # pop the number of items to roll off the stack
    position = opPop ()                 # pop the roll position number off the stack
    opstack[-number:] = opstack[-position:] + opstack[:-position]     # rotate the sublist by the position

def opCopy ():
    number = opPop ()                   # pop the number of items to copy off the stack
    opstack.extend (opstack[-number:])  # extend the opstack by a sublist of the opstack determined by the number

def opClear ():
    opstack.clear ()                    # clear the stack

def opStack ():
    index = len (dictstack) - 1                 # start the index count with the length of the dictstack - 1
    print ("==============")
    for x in reversed (opstack):                # loop through each item in the reversed opstack to print from the top down
        print (x)                               # print out the items one by one
    print ("==============")
    for t in reversed (dictstack):              # loop through each tuple in the reversed dictstack to print from the top down
        print ("---- %s ---- %s ----" % (index, staticCount))       # print out the dictstack index and static link
        for k, v in t[1].items ():              # for each key and value in the tuple's dictionary
            print (k, v)                        # print out the key and its value
        index -= 1                              # decrement the index of the dictstack
    print ("==============")
    
# Define the dictionary manipulation operators: def

def dsDef ():
    value = opPop ()                            # pop the variable value off the operand stack
    name = opPop ()                             # pop the variable name off the operand stack
    parse = name[1:]                            # parse the string to get rid of the /
    addDict = {parse : value}                   # create a new dictionary entry

    if not dictstack:                           # if the dictstack is empty
        dictstack.append ((staticCount, {}))    # append an empty tuple so we can start using it immediately
            
    for t in dictstack[-1:]:                    # for the top tuple in the dictionary stack
        t[1][parse] = value                     # add in the new dictionary entry

#*************************PART 2 CODE*************************
import re

# this function will take in a string of commands and tokenize them into a list
def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[(][a-zA-Z0-9_\s!][a-zA-Z0-9_\s!]*[)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

# this function will take in a list of tokens and create sublists
# based on tokens between curly braces
def groupMatching (it):
    res = []
    for c in it:                        # loop through the list of tokens
        if c == '}':                    # if we find an ending curly brace we are at the end of the sublist
            return res                  # return the sublist
        elif c == '{':                  # if we find an opening curly brace we are starting a new sublist
            res.append (groupMatching (it))                 # append the new sublist
        elif checkInt (c):              # check for a strng that we need to convert to an int
            newInt = int (c)            # convert the string to an int and store the int in newInt
            res.append (newInt)         # add the newInt to the res list
        else:
            res.append (c)              # otherwise just append the item to the result

# function for checking if a string is an int
def checkInt (x):
    if x[0] == '-':                     # first check for negative signs
        return x[1:].isdigit ()         # if there is a negative sign, ignore the first character
    return x.isdigit ()                 # otherwise just return if s is a digit or not

# this function will take in a list of tokens, it will call the
# groupMatching () function to create sublists for code arrays and for loops.
# it will also convert strings to ints outside of code arrays
def parse (s):
    parsed = []                         # local variable for storing the parsed tokens
    iterator = iter (s)                 # create the iterator for the list
    for x in iterator:                  # loop through the list of tokens
        if x == '{':                    # if we encounter an open curly brace
            parsed.append (groupMatching (iterator))      # call the groupMatching function to group the sublist
        elif checkInt (x):              # check for a string that we need to convert to an int outside of code arrays
            newInt = int (x)            # convert the string to an int
            parsed.append (newInt)      # add the newInt to the list
        else:
            parsed.append (x)           # otherwise just append the item to the parsed list
    return parsed

def forLoops ():
    code = opPop ()                     # pop the code array off the stack
    final = opPop ()                    # pop the final value off the stack
    incr = opPop ()                     # pop the increment off the stack
    init = opPop ()                     # pop the initial value off the stack
    opPush (init)                       # need to store the init value on the stack to execute the for loop

    if init > final:                    # if we're counting down
        while init > final:
            interpret (code)
            init += incr
            if init > final:            # don't want to push the init at the last iteration
                opPush (init)           # push the index on the stack
            else: break
            
    elif init < final:                  # if we're counting up
        while init < final:
            interpret (code)
            init += incr
            if init > final:            # don't want to push the init at the last iteration
                opPush (init)           # push the index on the stack
            else: break

def reset ():                           # clear the opstack and dictstack
    opstack.clear ()
    dictstack.clear ()                  

def interpret (tokens, rule):
    for x in tokens:
        if x == "add":
            opAdd ()
        elif x == "sub":
            opSub ()
        elif x == "mul":
            opMul ()
        elif x == "div":
            opDiv ()
        elif x == "mod":
            opMod ()
        elif x == "length":
            opLength ()
        elif x == "get":
            opGet ()
        elif x == "put":
            opPut ()
        elif x == "getinterval":
            opGetInterval ()
        elif x == "dup":
            opDup ()
        elif x == "exch":
            opExch ()
        elif x == "pop":
            opPopRemove ()
        elif x == "roll":
            opRoll ()
        elif x == "copy":
            opCopy ()
        elif x == "clear":
            opClear ()
        elif x == "stack":
            opStack ()
        elif x == "def":
            dsDef ()
        elif x == "for":
            forLoops ()
        elif not isinstance (x, list):        # don't want to call lookup () on a list
            if lookup (x, rule):              # if the varible name is in the dictstack
                opPush (lookup (x, rule))     # push its value on the stack
            else:
                opPush (x)                    # otherwise it's a new variable, push the name
        else: opPush (x)                      # case: it's a code array

def interpreter(s, rule):               # s is a string, rule is either static or dynamic scoping
    reset ()
    interpret(parse(tokenize(s)), rule)
    
#*************************TEST CODE*************************
# test the operand stack and its operations
def testOpPush ():
    opPush (5)
    opPush (6)
    if opPop () != 6: return False
    if opPop () != 5: return False
    return True

def testOpPop ():
    opPush ("/x")
    if opPop () != "/x": return False

    opPush ([{"x" : 5}, {"y" : 6}, {"z", 7}])
    if opPop () != [{"x" : 5}, {"y" : 6}, {"z", 7}]: return False
    return True

# test the dictionary stack and its operations
def testDictPush ():
    dictPush ({})
    if dictPop () != {}: return False

    dictPush ({"x" : 5, "y" : 6, "z" : 7})
    if dictPop () != {"x" : 5, "y" : 6, "z" : 7}: return False
    return True

def testDictPop ():
    dictPush ({"x" : 5, "y" : 6, "z" : 7})
    if dictPop () != {"x" : 5, "y" : 6, "z" : 7}: return False

    dictPush ({"x" : 5, "y" : 6, "z" : 7})
    dictPush ({"x" : 5, "y" : 6, "z" : 7})
    if dictPop () != {"x" : 5, "y" : 6, "z" : 7}: return False
    return True

def testDefine ():
    if define ("x", 5) != {"x" : 5}: return False
    if define ("","") != {"" : ""}: return False
    return True

# test all the arithmetic operators here -- add, sub, mul, div, mod
def testOpAdd ():
    opPush (50)
    opPush (50)
    opAdd ()
    if opPop () != 100: return False

    opPush (-5)
    opPush (5)
    opAdd ()
    if opPop () != 0: return False
    return True

def testOpSub ():
    opPush (50)
    opPush (50)
    opSub ()
    if opPop () != 0: return False

    opPush (-5)
    opPush (5)
    opSub ()
    if opPop () != 10: return False
    return True

def testOpMul ():
    opPush (50)
    opPush (50)
    opMul ()
    if opPop () != 2500: return False

    opPush (-5)
    opPush (5)
    opMul ()
    if opPop () != -25: return False
    return True

def testOpDiv ():
    opPush (50)
    opPush (50)
    opDiv ()
    if opPop () != 1: return False

    opPush (-5)
    opPush (5)
    opDiv ()
    if opPop () != -1: return False
    return True

def testOpMod ():
    opPush (50)
    opPush (50)
    opMod ()
    if opPop () != 0: return False

    opPush (5)
    opPush (26)
    opMod ()
    if opPop () != 1: return False
    return True

# test all the string operators -- length, get, put, getinterval
def testOpLength ():
    opPush ("(I love CptS 355!)")
    opLength ()
    if opPop () != 16: return False

    opPush ("()")
    opLength ()
    if opPop () != 0: return False
    return True

def testOpGet ():
    opPush ("(I love CptS 355!)")
    opPush (0)
    opGet ()
    if opPop () != 73: return False
    return True

def testOpPut ():
    opPush ("(I love CptS 355!)")
    opPush (0)
    opPush (105)
    opPut ()
    if opPop () != "i love CptS 355!": return False
    return True

def testGetInterval ():
    opPush ("(I love CptS 355!)")
    opPush (0)
    opPush (6)
    opGetInterval ()
    if opPop () != "I love": return False
    return True

# test the stack manipulation and print operators: dup, exch, pop, roll, copy, clear, stack
def testOpDup():
    opPush ("I love CptS 355!");
    opDup ()
    if opPop () != "I love CptS 355!": return False
    if opPop () != "I love CptS 355!": return False
    return True

def testOpExch ():
    opPush ("I love CptS 355!");
    opPush ("I love CptS 360!");
    opExch ()
    if opPop () != "I love CptS 355!": return False
    return True

def testOpPopRemove ():
    opPush ("I love CptS 355!");
    opPush ("I love CptS 360!");
    opPopRemove ()
    if opPop () != "I love CptS 355!": return False
    return True

def testOpRoll ():
    opPush (5)
    opPush (6)
    opPush (7)
    
    opPush (1)
    opPush(2)
    opRoll ()
    if opPop () != 6: return False
    return True

def testOpCopy ():
    opPush ("a")
    opPush ("b")
    opPush ("c")
    opPush (3)
    opCopy ()
    if opPop () != "c": return False
    if opPop () != "b": return False
    if opPop () != "a": return False
    if opPop () != "c": return False
    if opPop () != "b": return False
    if opPop () != "a": return False
    return True

def testOpClear ():
    opPush ("a")
    opPush ("b")
    opPush ("c")
    opClear ()
    if opstack != []: return False
    return True

def testOpStack ():
    opPush ("a")
    opPush ("b")
    opPush ("c")
    opPush ({"a" : 5})
    #opStack ()
    if opstack != ["a", "b", "c", {"a" : 5}]: return False
    opClear ()
    return True

def testDynamic ():
    interpreter (
    """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
    """, "dynamic")

    if opstack[0] != 7: return False

    interpreter (
    """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n (n in egg1) } def
    /chic 
            {/n 1 def 
             /egg2 {n (n in egg2) } def
             m (m in chic) n (n in chic)
             egg1
             egg2
             stack} def
    n  (n in main) 
    chic
    """, "dynamic")

    if opstack[0] != 100 and opstack[2] != 50 and opstack[4] != 1 and opstack[6] != 1 and opstack[9] != 1: return False

    interpreter (
    """
    /y 11 def
    /x 8 def
    /g { /x 10 def x stack } def
    /f { /y 3 def g } def
    /h { /x 100 def f } def
    h
    """, "dynamic")

    if opstack[0] != 10: return False
    
    return True

def testStatic ():
    interpreter (
    """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
    """, "static")

    if opstack[0] != 4: return False

    interpreter (
    """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n (n in egg1) } def
    /chic 
            {/n 1 def 
             /egg2 {n (n in egg2) } def
             m (m in chic) n (n in chic)
             egg1
             egg2
             stack} def
    n  (n in main) 
    chic
    """, "static")

    if opstack[0] != 100 and opstack[2] != 50 and opstack[4] != 100 and opstack[6] != 100 and opstack[9] != 100: return False

    interpreter (
    """
    /y 11 def
    /x 8 def
    /g { /x 10 def x stack } def
    /f { /y 3 def g } def
    /h { /x 100 def f } def
    h
    """, "static")

    if opstack[0] != 8: return False
    
    return True

def main ():
    testCases = [('opPush', testOpPush), ('opPop', testOpPop),
                 ('dictPush', testDictPush), ('dictPop', testDictPop),
                 ('define', testDefine), ('add', testOpAdd), ('sub', testOpSub),
                 ('mul', testOpMul), ('div', testOpDiv),
                 ('mod', testOpMod), ('opLength', testOpLength),
                 ('opGet', testOpGet), ('opPut', testOpPut),
                 ('opGetInterval', testGetInterval),
                 ('opDup', testOpDup), ('opExch', testOpExch),
                 ('opPopRemove', testOpPopRemove), ('opRoll', testOpRoll),
                 ('opCopy', testOpCopy), ('opClear', testOpClear),
                 ('opStack', testOpStack), ('testDynamic', testDynamic),
                 ('testStatic', testStatic)]

    listTestCases = [testOpPush, testOpPop, testDictPush, testDictPop,
                     testDefine, testOpAdd, testOpSub,
                     testOpMul, testOpDiv, testOpMod, testOpLength,
                     testOpGet, testOpPut, testGetInterval, testOpDup,
                     testOpExch, testOpPopRemove, testOpRoll, testOpCopy,
                     testOpClear, testOpStack, testDynamic, testStatic]
    
    for test in listTestCases:
        if not test(): print ("False")

    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        print ('Some tests failed', failedTests)
    else: print ('All tests OK')

if __name__ == "__main__":
    main()
