from graph import Graph

def returna(a, b):
	return a
	
def returnb(a, b):
	return b
	
def invert(a, b):
	return b, a

def link(a, b):
	a.graph.add(a.word, b.word)
	
def run_function_list(l, args):
	for fun in l:
		out = fun(*args)
		if out is not None:
			args = out
	return args

class WordType(object):
	def __init__(self, word, graph):
		self.word = word
		self.graph = graph

	def __str__(self):
		return repr(self)

	def __repr__(self):
		return "%s(%s)" % (type(self).__name__, self.word)
	

class Instantiating(WordType):
	def instantiate(self, word):
		return self.graph.add('', word)
	def __init__(self, word, graph):
		self.graph = graph
		self.word = self.instantiate(word)
	
class Determiner(WordType): pass
class Adjective(Instantiating): pass
class Adverb(Instantiating): pass
class Verb(Instantiating): pass
class Noun(Instantiating): pass

lookup_table = {
	"the":Determiner,
	"dog": Noun,
	"cat": Noun,
	"chases": Verb,
	"quickly": Adverb,
	"blue": Adjective,
	"green": Adjective,
	"bright": Adjective,
}
class WordNotFound(KeyError): pass

def classify(word, graph):
	try:
		wt = lookup_table[word]
	except KeyError:
		raise(WordNotFound(word))
	return wt(word, graph)


## for shorthand & memory efficiency:
linkab = (link, returna)
linkab_b = (link, returnb)
linkba = (invert, link, returna)

main_pair_actions = {
	Determiner:{
		Noun: linkba,
	},
	Adjective:{
		Adjective: linkba,
		Noun: linkba,
		Verb: linkba,
	},
	Adverb:{
		Adverb: linkba,
		Verb: linkba,
	},
	Verb:{
		Noun: linkab,
	},
	Noun:{
		Verb: linkab_b,
	},
}

outstanding = []


def clearout(l):
	try:
		a, b = l[-2:]
	except ValueError:
		return
	try:
		actions = main_pair_actions[type(a)]
	except:
		raise(TypeError("Unknown type: %s", type(a)))
	try:
		funlist = actions[type(b)]
	except:
		return
	l[-2:] = run_function_list(funlist, (a,b)),
	clearout(l)
	
def parse_sentence(sentence):
	g = Graph()
	for word in sentence.split():
		word = classify(word, g)
		outstanding.append(word)
		clearout(outstanding)
	return g
	
if __name__ == "__main__":
	print parse_sentence("the dog chases the blue cat")