from sentence_grapher import *

class Meanings(WordMeanings):
	pretable = """
	what the a: determiner
	dog cat color: noun
	red quickly brown: adj
	chases is: verb
	"""
	def noun(self, word):
		instance = self.instantiate(word)
		yield Store("noun instance", instance)
		yield Store("active", instance)
		
	def verb(self, word):
		instance = self.instantiate(word)
		print "hop"
		yield Store("verb instance",instance)
		print "hop1"
		yield Store("active", instance)	
		print "hop2"

		noun1 = yield Pull("noun instance", alreay_in_dict=True)
		print "hop3"
		noun2 = yield Pull("noun instance", alreay_in_dict=False, optional=True)
		print "hop4"

		self.graph.add(noun1, instance)
		if noun2:
			self.graph.add(instance, noun2)
			
	def determiner(self, word):
		print ":("
		yield Store("active", None)
		noun_instance = yield Pull("noun instance", alreay_in_dict=False)
		self.graph.add(word, noun_instance)
		print "yo"
		print "yo1"
		
	def adj(self, word):		
		instance = self.instantiate(word)
		print "ll"
		active = yield Pull("active")
		print '111'
		#if self.graph.has_edges(active, "*", "noun"):
		#	print "oh la la, its a noun"
		self.graph.add(active, instance)


def sentence_to_graph(sentence):
	wm = Meanings()
	d = Datastore()
	for word in sentence.split(" "): # use better splitting function later
		wm.start_action(word, d)
	
	d.checkout()
	return wm.graph


if __name__ == "__main__":
	from magicate import prettify
	
	g = sentence_to_graph("what color is the red dog")
	print prettify(g)