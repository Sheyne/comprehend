class graph(object):
	def __init__(self):
		self.edges = set()
		self.references = {}
		self._unique_num = 0
	
	def unique_num():
		self._unique_num += 1
		return self._unique_num

	def refers(key, node = None):
		if node:
			self.references[key] = node
			return node
		else:
			return self.references[key]

	def _add(a, b):
		self.edges.add(self.specialize(a,b))
	
	def keypop(self, keys, a):
		if keys:
			self.refers(keys.pop(0), a)

	def add(*nodes, keys = tuple()):
		nodes = list(nodes)
		keys = list(keys)
		a = nodes.pop(0)
		self.keypop(keys, a)
		for i in nodes:
			self._add(a,i)
			a = i
			self.keypop(keys, a)

	def _specialize(self, a):
		if a == "":
			return "anon/%s" % self.unique_num()
		elif a == "type":
			return "type/%s" % self.unique_num()
		else:
			return a
		
	def specialize(self, *a):
		return tuple(self._specialize(b) for b in a)
	
	@property
	def nodes(self):
		return set(n for e in self.edges for n in e)
