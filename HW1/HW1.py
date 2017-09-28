# Alexander Lao
# Intended for Windows

# returns a dictionary defined by mapping a char
# in s1 to the corresponding char in s2
# PRECONDITION: s1 and s2 must be the same length
def makettable (s1, s2):
    dictionary = dict (zip (s1, s2))
    return dictionary

# loops through each char in s and replaces them with
# their values if they exist in the ttable. chars are kept
# the same if their keys do not exist in the ttable.
# returns the modified string
def trans (ttable, s):
    for c in s:
        s = s.replace (c, ttable.get (c,c))
    return s

# tests the trans () function with unique strings that
# contain both upper and lower case letters
def testtrans ():
    ttable = makettable ('TuRkEy', 'MoNkEy')
    revttable = makettable ('MoNkEy', 'TuRkEy')
    teststring = "Animal: TuRkEy"
    expectedstring = "Animal: MoNkEy"
    
    if trans (ttable, teststring) != expectedstring:
        return False
    if trans (revttable, trans (ttable, teststring)) != teststring:
        return False
    if trans (ttable, ' ') != ' ':
        return False
    if trans (makettable ('   ', '   '), 'MoNkEy') != 'MoNkEy':
        return False
    return True

# creates a histogram list based on the most frequent char
# that appears in the string s. this function is adapted to help
# the digraphs () function; appending ('/' + c + '/') vs. appending (c)
# and sorting alphabetically vs. sorting alphabetically and
# then sorting based on frequency
def histo (s, digraph):
    freq = []
    seen = []
    
    for c in s:
        if c in seen:
            pass
        elif c not in seen and digraph == False:
            freq.append ((c, s.count (c)))
            seen.append (c)
        elif c not in seen and digraph == True:
            freq.append (('/' + c + '/', s.count (c)))
            seen.append (c)
            
    sortedhisto = sorted (freq, key = lambda item : item[0])

    if digraph == False:
        sortedhisto = sorted (sortedhisto, key = lambda item : item[1], reverse = True)
        
    return sortedhisto

# tests the histo () function with a regular string,
# a backwards string, and a string with both upper and
# lower case characters
def testhisto ():
    firststring = "aaabbbcccddd"
    firsthisto = [('a', 3), ('b', 3), ('c', 3), ('d',3)]
    secondstring = "dddcccbbbaaa"
    secondhisto = [('a', 3), ('b', 3), ('c', 3), ('d',3)]
    thirdstring = "BbBaAaDdDcCc"
    thirdhisto = [('B', 2), ('D', 2), ('a', 2), ('c', 2),
                  ('A', 1), ('C', 1), ('b', 1), ('d', 1)]
    
    if histo (firststring, False) != firsthisto:
        return False
    if histo (secondstring, False) != secondhisto:
        return False
    if histo (thirdstring, False) != thirdhisto:
        return False
    return True

# creates a digraph from a string. histo () will split
# the string into pairs of characters and put them into a list.
# the histo () function is then called on the list of pairs in order
# to determine their frequency and sort them
def digraphs (s):
    split = [s[i:i+2] for i in range (0, len (s) - 1, 1)]
    return histo (split, True)  

# tests the digraphs () function using a string with an even
# number of characters, an odd number of characters, and a
# string with only one unique character
def testdigraphs ():
    firststring = "aaabbbcccddd"
    firstdigraph = [('/aa/', 2), ('/ab/', 1), ('/bb/', 2), ('/bc/', 1),
                    ('/cc/', 2), ('/cd/', 1), ('/dd/', 2)]
    secondstring = "abc"
    seconddigraph = [('/ab/', 1), ('/bc/', 1) ]
    thirdstring = "          " # 10 spaces
    thirddigraph = [('/  /', 9)]

    if digraphs (firststring) != firstdigraph:
        return False
    if digraphs (secondstring) != seconddigraph:
        return False
    if digraphs (thirdstring) != thirddigraph:
        return False
    return True

if __name__ == '__main__':
    passedMsg = "%s passed"
    failedMsg = "%s failed"
    if testtrans () and testhisto () and testdigraphs ():
       print ( passedMsg % 'testtrans, testhisto, testdigraphs' )
    elif testtrans () == False:
       print ( failedMsg % 'testtrans' )
    elif testhisto () == False:
       print ( failedMsg % 'testhisto' )
    elif testdigraphs () == False:
       print ( failedMsg % 'testdigraphs' )
