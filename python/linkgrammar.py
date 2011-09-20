import locale
import clinkgrammar as clg

PRINT_DEBUG_STATEMENTS=False

class lp(object):
	@property
	def version(self):
		return clg.linkgrammar_get_version()

class ParseOptions(object):
	def __init__(self):
		if PRINT_DEBUG_STATEMENTS: print  "Creating",self.__class__
		self._po = clg.parse_options_create()
		clg.parse_options_set_verbosity(self._po,0)
	
	def __del__(self):
		if PRINT_DEBUG_STATEMENTS: print  "Deleting",self.__class__
		if self._po is not None:
			clg.parse_options_delete(self._po)
			self._po = None

class Dictionary(object):
	def __init__(self,lang):
		locale.setlocale(locale.LC_ALL,"en_US")
		self.parse_options = ParseOptions()
		if PRINT_DEBUG_STATEMENTS: print  "Creating",self.__class__
		self._dict = clg.dictionary_create_lang(lang)
		
	def Sentence(self, sentence):
		return Sentence(self,sentence)
	
	def __del__(self):
		if PRINT_DEBUG_STATEMENTS: print  "Deleting",self.__class__
		if self._dict is not None:
			clg.dictionary_delete(self._dict)
			self._dict = None
			
class Sentence(object):
	
	def __init__(self,dictionary,s):
		self.s = s
		self.dictionary=dictionary
		if PRINT_DEBUG_STATEMENTS: print  "Creating",self.__class__
		self._sent = clg.sentence_create(s,self.dictionary._dict)
	
	def __del__(self):
		if PRINT_DEBUG_STATEMENTS: print  "Deleting",self.__class__
		if self._sent is not None:
			clg.sentence_delete(self._sent)
			self._sent = None

	@property
	def linkages(self):
		self.parse()
		for idx in range(self.num_links):
			yield Linkage(idx,self)

	def parse(self):
		self.num_links = clg.sentence_parse(self._sent,self.dictionary.parse_options._po)
		return self.num_links

class LinkType(object):
	def __init__(self, mayjor, minors=None):
		if minors==None:
			self.mayjor=""
			self.minors=[]
			for x in mayjor:
				if x.lower()!=x:
					self.mayjor+=x
				else:
					self.minors.append(x)
		else:
			self.mayjor=mayjor
			self.minors=minors
	def __str__(self):
		return self.mayjor+str(self.minors)
	def __repr__(self):
		return "LinkType(type=%s, subtypes=%s)" % (repr(self.mayjor), repr(self.minors))

class Link (object):
	def __init__(self, left, right, type):
		self.left=left
		self.right=right
		self.type=type
		self.left.link_to(self, True)
		self.right.link_to(self, False)

	def __str__(self):
		return "%s <-%s-> %s" % (self.left, self.type, self.right)
	def __repr__(self):
		return "Link(left=%s,right=%s,type=%s)" % (repr(self.left), repr(self.right), repr(self.type))

class Word (object):
	def __init__(self, word, word_original):
		self.word=word
		self.word_original=word_original
		try:
			self.type=word.split(".")[1]
		except IndexError:
			self.type=False
	def link_to(self, link, direction=True):
		##a direction of True means `self` is the left of the link. (Link points right).
		tup=(link, direction)
		try:
			if not tup in self.links:
				self.links.append(tup)
		except AttributeError:
			self.links=[tup]
	def __str__(self):
		return self.word_original + ("[%s]" %self.type if self.type else "")
	def __repr__(self):
		return "Word(word=\"%s\", word_original=\"%s\")" % (self.word, self.word_original)

class Wall(Word):
	def __init__(self, type=False):
		##type false left, true right
		self.type=type
	def __str__(self):
		return "[right wall]" if self.type else "[left wall]"
	def __repr__(self):
		return "Wall(type=%s)" % self.type
class Punctuation(Word):
	def __init__(self, type='.'):
		self.type=type
	def __str__(self):
		return self.type
	def __repr__(self):
		return "Punctuation(type=\"%s\")" % self.type


class Linkage(object):
	def __init__(self,idx,sentence,setup_links=True):
		self.idx = idx
		self.sent = sentence
		if PRINT_DEBUG_STATEMENTS: print  "Creating",self.__class__
		self._link = clg.linkage_create(idx,sentence._sent,sentence.dictionary.parse_options._po)
		if setup_links: self.setup_links()

	def __del__(self):
		if PRINT_DEBUG_STATEMENTS: print  "Deleting",self.__class__
		if self._link is not None:
			clg.linkage_delete(self._link)
			self._link = None
		
	def num_sublinkages(self):
		return clg.linkage_get_num_sublinkages(self._link)

	def num_links(self):
		return clg.linkage_get_num_links(self._link)
	def num_words(self):
		return clg.linkage_get_num_words(self._link)

	def set_current_sublinkage(self, idx):
		clg.linkage_set_current_sublinkage(self._link, idx)
	
	def sublinkages(self):
		for idx in range(self.num_sublinkages()):
			self.set_current_sublinkage(idx)
			yield idx
	
	def link_right_word(self, idx):
		return clg.linkage_get_link_rword(self._link, idx)

	def link_left_word(self, idx):
		return clg.linkage_get_link_lword(self._link, idx)

	def link_label(self, idx):
		return clg.linkage_get_link_label(self._link, idx)

	def link_indexes(self):
		for idx in range(self.num_links()):
			yield idx

	def word_iterator(self):
		for idx in range(self.num_words()):
			w=clg.linkage_get_word(self._link, idx);
			if w=="LEFT-WALL":
				word=Wall(type=False)
			elif w=="RIGHT-WALL":
				word=Wall(type=True)
			elif len(w)==1 and w in '~!@#$%^&*()`-=_+[]\\{}|;\':",./<>?':
				word=Punctuation(type=w)
			else:
				word=Word(w, clg.sentence_get_word(self.sent._sent, idx))
			yield word

	def setup_links(self):
		self._links=[]
		for idx in self.link_indexes():
			link=Link(left=self.words[self.link_left_word(idx)],
					 right=self.words[self.link_right_word(idx)],
					  type=LinkType(mayjor=self.link_label(idx)))
			self._links.append(link)
			

	def setup_words(self):
		self._words=list(self.word_iterator())

	@property
	def links(self):
		try:
			return self._links
		except AttributeError:
			self.setup_links()
			return self._links

	@property
	def words(self):
		try:
			return self._words
		except AttributeError:
			self.setup_words()
			return self._words

	def __str__(self):
		return clg.linkage_print_diagram(self._link)