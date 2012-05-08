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

class AnyWordType(WordType): pass	
class Determiner(WordType): pass

class Instantiating(WordType):
	def instantiate(self, word):
		return self.graph.add('', word)
	def __init__(self, word, graph):
		self.graph = graph
		self.word = self.instantiate(word)
	
class Adjective(Instantiating): pass
class Adverb(Instantiating): pass
class Verb(Instantiating): pass
class Noun(Instantiating): pass

lookup_table = {
	"the":Determiner,
	"dog": Noun,
	"cat": Noun,
	"chases": Verb,
	"climbs": Verb,
	"quickly": Adverb,
	"blue": Noun,
	"green": Noun,
	"bright": Noun,
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
		Noun: linkab_b,
	},
	Noun:{
		Noun: linkab_b,
		Verb: linkab,
	},
	Adverb:{
		Adverb: linkab,
		Verb: linkab,
	},
	Verb:{
		Noun: linkab,
	},
}

class DefinitionNotFound(TypeError):
	def __str__(self):
		return "No definition found for: " + ", ".join(t.__name__ for t in self.args)

def parse_sentence(sentence):
	g = Graph()
	lastword = None
	for word in reversed(sentence.split()):
		word = classify(word, g)
		if lastword is not None:
			try:
				actions = main_pair_actions[type(word)]
			except KeyError:
				raise(DefinitionNotFound(type(word), AnyWordType))

			try:
				funlist = actions[type(lastword)]
			except KeyError:
				raise(DefinitionNotFound(type(word), type(lastword)))
			
			lastword = run_function_list(funlist, (word,lastword))
		else:
			lastword = word

	return g
	
if __name__ == "__main__":
	res = parse_sentence("the bright green dog chases the blue cat") 
	from magicate import prettify
	print prettify(res)
