import uuid


def _node_replace(node, old, new):
	"""
		If node is a value in `old`, return the value of `new` at the same position as the position of `old` that matches `node`. 
		
		`node` = the existing node
		`old` = iterable of values to compare node to
		`new` = iterable of what to return if node == old
		
		Example:
		>>> _node_replace('a', ('a','b'), ('c','d'))
		'c'
	"""
	for old_n, new_n in zip(old, new):
		if old_n == node:
			return new_n
	return node

def _nodes_replace(edge, old, new):
	""" Take an edge, replace valuse of `old` with `new` on each node in `edge`. 
		"""
	return tuple(_node_replace(node, old, new) 
				 for node in edge)

def _edge_replace(edges, old, new):
	"""Take a set of edges, replace all nodes that equal a value of `old` with the corresponding value in `new`. """
	return tuple(_nodes_replace(edge, old, new)
				 for edge in edges)

def make_loose_matching(edges):
	"""Take anonymous nodes and make them match any anonymous node by replacing "@" with "~". """
	
	ret = set(tuple(n.replace("@","~",1)
					 if n.startswith("@")
					 else n for n in edge)
			   for edge in edges)
	return ret
	
def match(a,b):
	"""Return `b` if `b` matches `a`. Otherwise return `False`. 
		
		For a match to be `True`, one of the following must be satisfied: 
			`a` == `b`
			`a` is a loose anonymous node and `b` is an anonymous node. 
			`a` contains "?"
			`a` is "*"
		
		Example:
		>>> match('a', 'b')
		False
		>>> match('a', 'a')
		'a'
		>>> match('?a', 'b')
		'b'
		>>> match('*', 'b')
		'b'
		>>> match('~3476781', '@16712')
		'@16712'
		"""
	return (b if a == b
				or a.startswith("~") and b.startswith(("@", "~"))
				or "?" in a
				or a == "*"
			  else False)

class Graph(object):
	"""A graph is at it's core a set of edges. Edges are 2-tuples of nodes. The idea is that an edge: `(a, b)`, means that `a` points at `b`."""
	def __init__(self, edges = set()):
		"""Initialize the object. All this does is initialize the Edges instance variable to a copy of `edges`. """
		edges = edges if isinstance(edges, set) else set(edges)
		self.edges = edges.copy()
	
	def combine(self, target, action = set.union):
		"""Add the edges of the `target` graph to `self` with the union set operation. 
			
			Example:
			>>> g1 = Graph(('a', 'b'))
			>>> g2 = Graph(('c', 'd'))
			>>> g3 = g1.combine(g2)
			>>> g3.edges
			set(['a', 'c', 'b', 'd'])
			"""

		return Graph(action(self.edges, target.edges))
	
	def union(self, target, action = set.union):
		"""Add the edges of the `target` graph to `self` with the union set operation. If the action parameter is set, use a different set operation. 
			
			Example:
			>>> g1 = Graph(('a', 'b'))
			>>> g2 = Graph(('c', 'd'))
			>>> g1.union(g2)
			>>> g1.edges
			set(['a', 'c', 'b', 'd'])
			"""
		self.edges = action(self.edges, target.edges)
	
	def unique_num(self):
		"""Return a unique number. Currently returns a UUID based off the time. This should not be counted on. All you should count on is the number being unique and consisiting of letters and numbers."""
		return str(uuid.uuid4()).replace("-", "")

	def __add(self, a, b):
		"""Internal function to add an edge with (`a`, `b`). """
		self.edges.add(self.edge__specialize(a,b))
	
	def add(self, *nodes):
		"""Create edges for each combination of nodes.
			
			Example:
			>>> g = Graph()
			>>> g.add('a', 'b', 'c')
			>>> g.edges
			set([('a', 'b'), ('b', 'c')])
			"""
		nodes = list(nodes)
		a = nodes.pop(0)
		for i in nodes:
			self.__add(a,i)
			a = i

	def specialize(self, a):
		"""Internal method. It does the syntactical sugar. """
		nodes = a.split(".")
		node_o = self.__specialize(nodes.pop(0))
		node_holder = node_o
		for node in nodes:
			node = self.__specialize(node)
			self.__add(node_holder, node)
			node_holder = node
		return node_o
		
	def __specialize(self, a):
		"""Helper method for `graph.specialize`. """
		if a == "" or a == "@":
			out = "@%s" % self.unique_num()
			self.__add(out, "anonymous+node")
		else:
			out = a
		self.last_specialized = out
		return out
		
	def edge__specialize(self, *a):
		"""Specialize all edges in iterator `a`."""
		return tuple(self.specialize(b) for b in a)
	
	@property
	def nodes(self):
		"""Return all nodes in an object. 
			
			Example:
			>>> g = Graph()
			>>> g.add('a', 'b')
			>>> g.nodes
			set(['a', 'b'])
			"""
		return set(n for e in self.edges for n in e)
	
	def match_edges(self, edge1, edge2):
		r = tuple(match(n1, n2) for n1, n2 in zip(edge1,edge2)) 
		return r if r[0] and r[1] else False

	def matching(self, e):
		"""Look for all edges matching `e`."""
		return [edge for edge in self.edges if self.match_edges(e, edge)]

	def query(self, q):
		""" Run a query graph on self.
			
			Returns a list of query restult dictionaries. A query result dictionay has query nodes as keys, and the values that they could be as values. 
			
			Example:
			>>> enviroment = Graph()
			>>> enviroment.add('a','b')
			>>> enviroment.add('c','d')
			>>> query1 = Graph()
			>>> query1.add('?', 'b')
			>>> enviroment.query(query1)
			[{'?': 'a'}]
			>>> query2 = Graph()
			>>> query2.add('?named_search', 'd')
			>>> enviroment.query(query2)
			[{'?named_search': 'c'}]

		"""
		
		self.solutions = []
		
		self.__query(tuple(make_loose_matching(q.edges)))
		return self.solutions
	
	def __query(self, edges, solutionset = {}, consumed_edges = set()):
		""" Recursive internal query method. """
		
		if not edges:
			self.solutions.append(solutionset)
		else:
			edge_, edges = edges[0], edges[1:]
			for edge in self.matching(edge_):
				if not edge in consumed_edges:
					solutionset = solutionset.copy()
					consumed_edges_c = consumed_edges.copy()
					consumed_edges_c.add(edge)
					for key, value in zip(edge_, edge):
						if "?" in key:
							solutionset[key] = value
					self.__query(_edge_replace(edges, edge_, edge), solutionset, consumed_edges_c)
	def dump(self, f):
		""" Write the graph to a file-like object. """
		for e in self.edges:
			f.write("%s\t%s\n" % (e[0], e[1]))

	def load(self, f):
		""" Load the graph from a file-like object. """
		for line in f:
			self.add(*line.split("\t"))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
