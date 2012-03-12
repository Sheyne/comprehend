import collections

def short_unique(L):
	L = list(set(L))
	if L:
		l = len(L[0])
		still_care_about = [True] * len(L)
		
		for i in xrange(l):
			qm = tuple(d[i] for d in L)
			counter = collections.Counter(qm)
			still_care_about = list(counter[qm[idx]]>1 and still_care_about[idx] for idx in xrange(len(L)))
			if collections.Counter(still_care_about)[True] <= 1:
				return i
		return l
	else:
		return 0
def _magi(t,i):
	return "" if t[1] == "anonymous+node" else "\n" + str(tuple(x[:i+1] if x.startswith("@") else x for x in t))

def prettify(c):
	out = c.edges
	l = short_unique([item for sl in out for item in sl if item.startswith("@")])
	return reduce(lambda x,y:str(x)+str(_magi(y, l)), out, "")
