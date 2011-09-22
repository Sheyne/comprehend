import linkgrammar
class Phrase(object):
	def __init__(self, words, main):
		self.main=main
		self.words=words
	@property
	def order(self):
		"""Return a tuple with index of each word. For example: (1,0), would mean 1st word 0th word."""
		absolute_positions=map(lambda word: word.position, self.words)
		sorted_positions = sorted(absolute_positions)
		hash_positions = {}
		
		for i in range(len(sorted_positions)):
			hash_positions[sorted_positions[i]]=i
		
		return map(lambda i: hash_positions[i], absolute_positions)

	def __str__(self):
		return "<%s>" % " ".join(map(lambda idx: str(self.words[idx]), self.order))

	def __repr__(self):
		return "Phrase(words=%s, main=%s)" % (repr(self.words), repr(self.main))
