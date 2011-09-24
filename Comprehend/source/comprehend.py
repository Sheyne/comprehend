import linkgrammar
import util

class Word(object):
	def __init__(self, link_word_object):
		self.word = link_word_object
	
	def __getattr__(self, attr):
		return self.word.__getattribute__(attr)
	
	@property
	def left_links(self):
		"""Returns a tuple of all links that point to the left."""
		filter()
		return ()
	
	@property
	def right_links(self):
		"""Returns a tuple of all links that point to the right."""
		#fill out
		return ()

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

class NounPhrase(Phrase):
	def __init__(self, word):
		self.main=word
		self.words=word,
		try:
			llinks=self.main.left_links
		except:
			self.main=Word(self.main)
			llinks=self.main.left_links
		
		print llinks
		
		for link in llinks:
			print link
		
def process_sentence(sent):
	dict=linkgrammar.Dictionary("en")
	sent = dict.Sentence(sent)

	for linkage in sent.linkages:
		print linkage
		subject = None
		object = None
		verb = None
		for link in linkage.links:
			if link.type.mayjor == "S":
				subject=link.left
				verb=link.right
		subject = NounPhrase(subject)
		print subject, verb
		break