# Alexander Lao
# Intended for Windows

# PART ONE: Lines 13 - 153
# PART TWO: Lines 155 - 278
# TEST CODE: Lines 280 - 555
# MAIN: Line 557
# Interpreter Function Call: Line 589
# NOTE: The function call 'fact' is being pushed to the operand stack.
#       It's being pushed on line 274, but it should be going into the
#       if-statement on line 271 and skipping the else-statement.

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

def dictPush ():
    newDict = opPop ()                  # pop the dictionary off the operand stack
    dictstack.append (newDict)          # add the new dictionary to the dictionary stack

def define (name, value):
    name = {name : value}               # store the dict entry in name
    return name

def lookup (name):
    for d in dictstack:                 # look at each dict in the dictstack
        if name in d:                   # search for the name in the dict
            if isinstance (d[name], list):  # if the name is associated with a code array
                interpret (d[name])     # call that function
            else: return d[name]        # otherwise just return the value associated with the name
        else: pass                      # if the name is not in the dictstack, do nothing

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
    opstack.reverse ()                  # reverse the stack to print from the top down
    print (*opstack)                    # print the stack, * to print items in the list
    opstack.reverse ()                  # return the stack to its original order
    
# Define the dictionary manipulation operators: dict, begin, end, def
def dsDict ():
    size = opPop ()                     # pop the size of the empty dictionary off the stack
    newDict = {}                        # create a new dictionary
    opPush (newDict)                    # push the new dictionary onto the operand stack

def dsBegin ():
    dictPush ()                         # call the dictPush () method

def dsEnd ():
    dictPop ()                          # call the dictPop () method

def dsDef ():
    value = opPop ()                    # pop the variable value off the operand stack
    name = opPop ()                     # pop the variable name off the operand stack
    parse = name[1:]                    # parse the string to get rid of the /
    addDict = {parse : value}           # create a new dictionary entry

    if not dictstack:                   # if the dictstack is empty
        dictstack.append ({})           # append an empty dictionary so we can start using it immediately
            
    for d in dictstack[-1:]:            # for the top dictionary in the dictionary stack
        d[parse] = value                # add in the new dictionary entry

#*************************PART 2 CODE*************************
import re

# this function will take in a string of commands and tokenize them into a list
def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[(][\w \W]*[)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

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

def interpret (tokens):
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
        elif x == "dict":
            dsDict ()
        elif x == "begin":
            dsBegin ()
        elif x == "end":
            dsEnd ()
        elif x == "def":
            dsDef ()
        elif x == "for":
            forLoops ()
        elif not isinstance (x, list):  # don't want to call lookup () on a list
            if lookup (x):              # if the varible name is in the dictstack
                opPush (lookup (x))     # push its value on the stack
            else:
                opPush (x)              # otherwise it's a new variable, push the name
        else: opPush (x)                # case: it's a code array

def interpreter(s):                     # s is a string
    interpret(parse(tokenize(s)))
    
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
    opPush ({})
    dictPush ()
    if dictPop () != {}: return False

    opPush ({"x" : 5, "y" : 6, "z" : 7})
    dictPush ()
    if dictPop () != {"x" : 5, "y" : 6, "z" : 7}: return False
    return True

def testDictPop ():
    opPush ({"x" : 5, "y" : 6, "z" : 7})
    dictPush ()
    
    if dictPop () != {"x" : 5, "y" : 6, "z" : 7}: return False

    opPush ({"x" : 5, "y" : 6, "z" : 7})
    dictPush ()
    
    opPush ({"x" : 5, "y" : 6, "z" : 7})
    dictPush ()
    
    if dictPop () != {"x" : 5, "y" : 6, "z" : 7}: return False
    return True

def testDefine ():
    if define ("x", 5) != {"x" : 5}: return False
    if define ("","") != {"" : ""}: return False
    return True

def testLookup ():
    opPush ({"x" : 5, "y" : 6, "z" : 7})
    dictPush ()
    
    opPush ({"a" : 8, "b" : 9, "c" : 10})
    dictPush ()
    
    if lookup ("x") != 5: return False
    if lookup ("b") != 9: return False
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
    opStack ()
    if opstack != ["a", "b", "c", {"a" : 5}]: return False
    opClear ()
    return True

# test the dictionary manipulation operators: dict, begin, end, def
def testDsDict ():
    opPush (5)
    dsDict ()
    if opPop () != {}: return False
    return True

def testDsBegin ():
    opPush (5)
    dsDict ()
    dsBegin ()
    if dictPop () != {}: return False
    return True

def testDsEnd ():
    dictstack.clear ()
    
    opPush (5)
    dsDict ()
    dsBegin ()
    dsEnd ()
    if len (dictstack) != 0: return False
    
    opPush (6)
    dsDict ()
    dsBegin ()

    opPush (7)
    dsDict ()
    dsBegin ()
    dsEnd ()
    if len (dictstack) != 1: return False
    return True

def testDsDef ():
    opPush (5)
    dsDict ()
    dsBegin ()

    opPush ("/x")
    opPush (5)
    dsDef ()

    opPush ("/y")
    opPush (6)
    dsDef ()

    opPush (5)
    dsDict ()
    dsBegin ()

    opPush ("/z")
    opPush (7)
    dsDef ()
    if dictPop () != {"z" : 7}: return False
    dictstack.clear ()
    return True

def main ():
    testCases = [('opPush', testOpPush), ('opPop', testOpPop),
                 ('dictPush', testDictPush), ('dictPop', testDictPop),
                 ('define', testDefine), ('lookup', testLookup),
                 ('add', testOpAdd), ('sub', testOpSub),
                 ('mul', testOpMul), ('div', testOpDiv),
                 ('mod', testOpMod), ('opLength', testOpLength),
                 ('opGet', testOpGet), ('opPut', testOpPut),
                 ('opGetInterval', testGetInterval),
                 ('opDup', testOpDup), ('opExch', testOpExch),
                 ('opPopRemove', testOpPopRemove), ('opRoll', testOpRoll),
                 ('opCopy', testOpCopy), ('opClear', testOpClear),
                 ('opStack', testOpStack), ('dsDict', testDsDict),
                 ('dsBegin', testDsBegin), ('dsEnd', testDsEnd),
                 ('dsDef', testDsDef)]

    listTestCases = [testOpPush, testOpPop, testDictPush, testDictPop,
                     testDefine, testLookup, testOpAdd, testOpSub,
                     testOpMul, testOpDiv, testOpMod, testOpLength,
                     testOpGet, testOpPut, testGetInterval, testOpDup,
                     testOpExch, testOpPopRemove, testOpRoll, testOpCopy,
                     testOpClear, testOpStack, testDsDict, testDsBegin,
                     testDsEnd, testDsDef]
    
    for test in listTestCases:
        if not test(): print ("False")

    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        print ('Some tests failed', failedTests)
    else: print ('All tests OK')

    interpreter(
    """
    /fact{
    0 dict
            begin
                    /n exch def
                    1
                    n -1 1 {mul} for
            end
    }def
    (factorial function !)  0 9 getinterval 
    stack
    5 fact 
    stack
    """
    )

if __name__ == "__main__":
    main()
