import linkgrammar
class Phrase(object):
	def __init__(self, words, main):
		self.main=main
		self.words=words
	@property
	def order(self):
		"""Return a tuple with index of each word. For example: (1,0), would mean 1st word 0th word."""
		#fill in
		return (0,1)
	def __str__(self):
		return " ".join(map(lambda idx: str(self.words[idx]), self.order))
	def __repr__(self):
		return "Phrase(words=%s, main=%s)" % (repr(self.words), repr(self.main))
dict=linkgrammar.Dictionary("en")
sent = dict.Sentence("The dog has brown fur.")
