from collections import deque
import graph as graphmodule

class PullError(Exception): pass

class Action(object):
	def __init__(self, *args):
		self.args = args
		self.arg = args[0] if len(args) == 1 else args
	
	def __str__(self):
		return str(self.arg)
		
	def __getitem__(self, i):
		return self.args[i]
	
	def finish(self, action_generator, datastore, send = None):
		try:
			if send is not None:
				nxt = action_generator.send(send)
			else:
				nxt = action_generator.next()
		except StopIteration:
			return
		nxt.do(action_generator, datastore)
		
	def do(self, action_generator, datastore):
		raise NotImplementedError("Method do not implemented on class: %s" % self.__class__.__name__)
	
class Store(Action):
	def __init__(self, key, value):
		super(Store, self).__init__(key, value)
		self.key = key
		self.value = value

	def do(self, action_generator, datastore):
		if self.value is not None:
			datastore[self.key] = self.value
		else:
			try:
				del datastore[self.key]
			except KeyError: pass
		self.finish(action_generator, datastore)

class Pull(Action):
	def __init__(self, key, alreay_in_dict = 'IDC', optional = False):
		super(Pull, self).__init__(key)
		self.key = key
		self.alreay_in_dict = alreay_in_dict
		self.optional = optional

	def _look_left(self, action_generator, datastore, override = False):
		try:
			value = datastore[self.key]
			if value is None:
				raise KeyError(self.key)
		except KeyError:
			if override and not self.optional:
				raise PullError("Requested word does not yet exist. ")

		self.finish(action_generator, datastore, value)

	def _look_right(self, action_generator, datastore):
		def han(value):
			self.finish(action_generator, datastore, value)
		
		han.action_generator = action_generator
		han.datastore = datastore
		han.action = self
		datastore.add_handle(self.key, han)
		
	def do(self, action_generator, datastore):
		if self.alreay_in_dict == 'IDC':
			try:
				self._look_left(action_generator, datastore, True)
			except PullError:
				self._look_right(action_generator, datastore)

		elif self.alreay_in_dict:
			self._look_left(action_generator, datastore)
		else:
			self._look_right(action_generator, datastore)

class Datastore(object):
	def __init__(self, *args):
		self.data = dict(*args)
		self.handles = {}

	def add_handle(self, key, handle):
		try:
			handle_list = self.handles[key]
		except KeyError:
			handle_list = deque()
			self.handles[key] = handle_list
		handle_list.appendleft(handle)
	
	def checkout(self):
		handles = self.handles
		for key in handles:
			val = handles[key]
			for han in val:
				act = han.action
				if act.optional:
					act.finish(han.action_generator, han.datastore)
					val.remove(han)
					
		hl = tuple((key, handles[key]) for key in handles if handles[key])
		if hl:
			raise PullError("Checking out, and requests remain. ", hl)
	
	def __setitem__(self, key, value):
		self.data[key] = value
		try:
			handle_list = self.handles[key]
			del self.handles[key]
		except KeyError:
			handle_list = tuple()
		
		for handle in handle_list:
			handle(value)
				
	def __getitem__(self, key):
		return self.data[key]
		
	def __delitem__(self, key):
		del self.data[key]
		

class WordMeanings(object):
	pretable = ''
	def __init__(self, graph = None):
		if graph:
			self.graph = graph
		else:
			self.graph = graphmodule.Graph()
				
		self.table = {}
		for line in self.pretable.splitlines():
			broken = line.split(":", 1)
			try:
				keys, value = broken
			except ValueError:
				continue
			keys = keys.split()
			value = value.strip()
			value = self.__getattribute__(value)
			for key in keys:
				self.table[key] = value
	
	def actions(self, word):
		return self.table[word](word)
	
	def start_action(self, word, datastore):
		gen = self.actions(word)
		gen.next().do(gen, datastore)
	
	def instantiate(self, word, token = "@"):
		instance = self.graph.specialize(token)
		self.graph.add(instance, word)
		return instance