from sentence_grapher import *

class Meanings(WordMeanings):
	pretable = """
	the: find_noun
	a: create_noun
	dog cat color tree fence: noun
	red quickly brown blue green up: adj
	chases is climbs circles: verb
	that: that
	"""
	def __init__(self, graph=None):
		super(Meanings, self).__init__(graph)
		self._lookup_index = -1

	def lookup_index(self):
		self._lookup_index += 1
		return str(self._lookup_index)

	def that(self, word):
		yield Store("terminate", False)

	def noun(self, word):
		instance = self.instantiate(word)
		yield Store("noun instance", instance)
		yield Store("active", instance)

		terminate = yield Pull("terminate", alreay_in_dict=False, optional=True)
		if terminate is not False:
			yield Store("lookup", None)

	def verb(self, word):
		tag = yield get_tag()
		yield Store("terminate", True)

		instance = self.instantiate(word)
		yield Store("verb instance",instance)
		yield Store("active", instance)	

		noun1 = yield prev_noun_instance()
		noun2 = yield next_noun_instance(optional=True)

		self.graph.add_tag(tag, noun1, instance)
		if noun2:
			self.graph.add_tag(tag, instance, noun2)

	def find_noun(self, word):
		yield deactivate()
		lookup_id = "lookup " + self.lookup_index()
		yield Store("lookup", lookup_id)
		noun_instance = yield next_noun_instance()
		self.graph.add("action+lookup", noun_instance)

	def create_noun(self, word): 
		if word == "a":
			word = "1"
		yield deactivate()
		noun_instance = yield next_noun_instance()
		self.graph.add(word, noun_instance)

	def adj(self, word):		
		active = yield Pull("active")
		instance = self.instantiate(word)
		#if self.graph.has_edges(active, "*", "noun"):
		#	print "oh la la, its a noun"
		self.graph.add(active, instance)


def parse_sentence(sentence):
	wm = Meanings()
	d = Datastore()
	for word in sentence.split(" "): # use better splitting function later
		wm.start_action(word, d)

	d.checkout()
	return wm.graph

def deactivate():
	return Store("active", None)

def noun_instance(already_exists="IDC", optional=False):
	return Pull("noun instance", alreay_in_dict=already_exists, optional=optional)	

def next_noun_instance(optional=False):
	return noun_instance(already_exists=False, optional=optional)

def prev_noun_instance(optional=False):
	return noun_instance(already_exists=True, optional=optional)

def get_tag():
	return Pull("lookup", alreay_in_dict=True, optional=True)
