import collections

import graph
import re
import mindnode


definitions = {}
dictionary = mindnode.mindmap('resources/dictionary.mindnode')


def add_definition(*names):
	def _add_definition(func):
		for name in names:
			definitions[name] = func
	return _add_definition

@add_definition("the")
def _(self, word):
	query = graph.Graph()
	query.add("?", "noun")
	noun_instance = self.graph.specialize("")
	@self.request((query, "?"), direction = Converter.DIRECTION_RIGHT, require = True)
	def _(result):
		self.graph.add(noun_instance, result)
	return noun_instance


@add_definition("dog", "cat")
def _(self, word):
	return word

@add_definition("chases", "ran")
def _(self, word):
	query = graph.Graph()
	query.add("?", "*34612")
	query.add("*34612", "noun")
	verb_instance = self.graph.specialize("")
	self.graph.add(verb_instance, word)
	
	@self.request((query, "?"), Converter.DIRECTION_LEFT, True)
	def _(result):
		self.graph.add(result, verb_instance)
	
	@self.request((query, "?"), Converter.DIRECTION_RIGHT, True)
	def _(result):
		print result
		self.graph.add(verb_instance, result)
	
	return verb_instance

@add_definition(".")
def _(self, word):
	return word

class Converter(object):
	puntuation_re = re.compile("\w+|[%s]" % re.escape(".?!"))
	DIRECTION_LEFT = "Left"
	DIRECTION_RIGHT = "Right"

	@classmethod
	def preprocess(cls, sent):
		return Converter.puntuation_re.findall(sent)

	def __init__(self, sentence):
		self.graph = dictionary.copy()
		self.requests = []
		self.emitted = []
		# will eventually need to account for planarity

		for word in Converter.preprocess(sentence):
			self.emitted.append(self.process(word))
			for idx in reversed(xrange(len(self.requests))):
				(query, key), handler, require = self.requests[idx]
				print key, query.edges, handler
				for match in self.graph.query(query):
					# need to account for planarity
					mqp = match[key]
					if mqp in self.emitted: # really need planarity now, recursive implemetation? 
						print ":", mqp, word
						handler(mqp)
						del self.requests[idx]
						break
		if any(req[2] for req in self.requests):
			raise LookupError("No right matches found. ")

	def request(self, query, direction = "Left", require = False):
		def _request(handler):
			if direction is Converter.DIRECTION_LEFT:
				q, key = query
				for match in self.graph.query(q):
					# need to account for planarity
					mqp = match[key]
					if mqp in self.emitted:
						handler(mqp)
						break
				else:
					if require:
						raise LookupError("No left matches found. ")
					
			elif direction is Converter.DIRECTION_RIGHT:
				self.requests.append((query, handler, require))
			else:
				raise ValueError("Unknown Direction")
		return _request


	def process(self, word):
		return definitions[word](self, word)

	def the_function(self):
		noun_instance = self.graph.specialize()
		# self.graph.add()

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
	return tuple(x[:i+1] if x.startswith("@") else x for x in t)

def magicate(c):
	out = c.graph.combine(dictionary, set.difference).edges
	l = short_unique([item for sl in out for item in sl if item.startswith("@")])
	return reduce(lambda x,y:str(x)+"\n"+str(_magi(y, l)), out, "")

if __name__ is "__main__":
	c = Converter("the dog chases the cat.")
	
	print magicate(c)