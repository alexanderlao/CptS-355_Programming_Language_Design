# Alexander Lao
# Intended for Windows

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
            return d[name]              # return the value associated with the name
        else:
            pass                        # if the name is not in the dictstack, do nothing

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
    length = 0                          # define a local counter to hold the length                            
    for x in string:                    # for every character in the string
        length += 1                     # add 1 to the length
    opPush (length)                     # push the length onto the stack

def opGet ():
    index = opPop ()                    # pop the index off the stack
    string = opPop ()                   # pop the string off the stack
    a = ord (string[index])             # convert the character at the string's index to its ascii value
    opPush (a)                          # push the ascii value onto the stack

def opPut ():
    value = opPop ()                    # pop the ascii value off the stack
    index = opPop ()                    # pop the index off the stack
    string = opPop ()                   # pop the string off the stack
    char = chr (value)                  # convert the ascii value to a character
    string = string[:index] + char + string[index + 1:]       # replacing the specified index in the string with the new character
    opPush (string)
    
def opGetInterval ():
    count = opPop ()                    # pop the count off the stack
    index = opPop ()                    # pop the index off the stack
    string = opPop ()                   # pop the string off the stack
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
    addDict = {parse, value}            # create a new dictionary entry
    
    for d in dictstack[-1:]:            # for the top dictionary in the dictionary stack
        d[parse] = value                # add in the new dictionary entry

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
    opPush ("I love CptS 355!")
    opLength ()
    if opPop () != 16: return False

    opPush ("")
    opLength ()
    if opPop () != 0: return False
    return True

def testOpGet ():
    opPush ("I love CptS 355!")
    opPush (0)
    opGet ()
    if opPop () != 73: return False
    return True

def testOpPut ():
    opPush ("I love CptS 355!")
    opPush (0)
    opPush (105)
    opPut ()
    if opPop () != "i love CptS 355!": return False
    return True

def testGetInterval ():
    opPush ("I love CptS 355!")
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

if __name__ == "__main__":
    main()
