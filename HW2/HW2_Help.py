def groupMatching(it):
    res = []
    for c in it:
        if c == ')':
            return res
	elif c == '(':
            res.append (groupMatching (it))
        else:
            res.append (c)
    return False

def test (it):
	nextItem = (next (it, None))
	if nextItem == None:
		return
	else:
		print (nextItem)
		test (it)

x = iter ([1,2,3,4,5,6,7])

# make sure the put operator starts at index 1 because strings will look like
# (This is my string!) index 0 will be the '('
