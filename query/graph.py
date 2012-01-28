class Node(object):	
	"""Provides a node class for a graph type data structure. """


	""" Standard Public Methods """

	def __init__(self, data):
		self.data = data
		self.edges = set()
	
	def point_at(self,*targets):
		for target in targets:
			self.add_edge((target, 1))
	def unpoint_at(self,*targets):
		for target in targets:
			self.remove_edge((target, 1))

	""" String Conversion """

	def __repr__(self):
		return "%s(%s)" % (type(self).__name__, repr(self.data))
	
	def __str__(self):
		return str(self.data)
	
	""" Advanced """
		
	def add_edge(self, edge):
		# check if the node is already targeted
		if not self.has_edge(edge):
			# and the edge to internal edge set
			self.edges.add(edge)
			# check if target reciprocates 
			reciprocal_edge = self.reciprocal_edge(edge)
			if not edge[0].has_edge(reciprocal_edge):
				edge[0].add_edge(reciprocal_edge)

	def remove_edge(self, edge):
		try:
			self.edges.remove(edge)
			# check if target reciprocates 
			try:
				edge[0].remove_edge(self.reciprocal_edge(edge))
			except KeyError:
				pass # target does not reciprocate
		except KeyError:
			raise KeyError(edge,"Does not have edge")
				
	def has_edge(self, edge):
		return edge in self.edges
	
	""" Helpers """
	
	def reciprocal_edge(self, edge):
		return (self, edge[1]*-1)
