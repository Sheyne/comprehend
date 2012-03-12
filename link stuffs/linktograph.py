import collections
import re

import linkgrammar
import parse.graph as graph
import questionformater


class TryAgainLater(Exception): pass

link_types = {}
def define(link_type):
	def _(func):
		def internal(*args):
			try:
				func(*args)
			except AttributeError as e:
				raise(TryAgainLater(e))
		link_types[link_type] = internal
	return _
		
transliterator_dictionary = """
define RW
	pass

define W
	pass

define A
	right.instance
	left.instance = s("")
	link(left.instance, left)
	link(right.instance, left.instance)

define D
	det = s("")
	link(det, left)
	right.instance = s("")
	link(right.instance, det)
	link(right.instance, right)

define S
	left.instance # essentially, check that the instance variable exists
	right.instance = s("")
	link(right.instance, right)
	link(left.instance, right.instance)

define O
	right.instance
	left.instance
	link(left.instance, right.instance)
"""

modified_dictionary = re.sub("^define[ ]+(\w+)[ ]*$",lambda x: """@define("%s")
def _(self, left, right):""" % x.group(1), transliterator_dictionary, flags = re.MULTILINE)

exec modified_dictionary


def short_unique(L):
	L = list(set(L))
	l = len(L[0])
	still_care_about = [True] * len(L)
	
	for i in xrange(l):
		qm = tuple(d[i] for d in L)
		counter = collections.Counter(qm)
		still_care_about = list(counter[qm[idx]]>1 and still_care_about[idx] for idx in xrange(len(L)))
		if collections.Counter(still_care_about)[True] <= 1:
			return i
	return l

def _magi(t,i):
	return "" if t[1] == "anonymous+node" else "\n" + str(tuple(x[:i+1] if x.startswith("@") else x for x in t))

def magicate(c):
	out = c.edges
	l = short_unique([item for sl in out for item in sl if item.startswith("@")])
	return reduce(lambda x,y:str(x)+str(_magi(y, l)), out, "")

def link(a,b):
	g.add(str(a), str(b))

def s(*a):
	return g.specialize(*a)


g = graph.Graph()

d = linkgrammar.Dictionary()
sen = linkgrammar.Sentence(d, "what color is the dog")

linkage = sen.linkages.next()

print linkage

def trylink(link):
	try: 
		f = link_types[link.type.mayjor]
	except KeyError:
		f = None
	
	if f:
		f(graph, link.left, link.right)
	else:
		raise(NameError("Link type: \"%s\" not found" % link.type))
	

def main():
	links = linkage.links
	laters = []
	for link in links:
		try:
			trylink(link)
		except TryAgainLater as e:
			laters.append(link)

	while laters:
		changed = False
		for idx, link in enumerate(laters):
			try:
				trylink(link)
			except TryAgainLater as e:
				print e
			else:
				del laters[idx]
				changed = True
		if (not changed) and laters:
			raise(AttributeError("Attributes are required, but they are not being set. "))

	
	print magicate(g)
	print questionformater.formatquestion(g)
if __name__ == "__main__":
	main()