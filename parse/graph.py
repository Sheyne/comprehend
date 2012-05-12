#! /usr/bin/env python2.7

import uuid

class TagError(KeyError): pass

def unique_num():
	return str(uuid.uuid4()).replace("-", "")

class Graph(object):
	"""A graph is at it's core a set of edges. Edges are 2-tuples of nodes. The idea is that an edge: `(a, b)`, means that `a` points at `b`."""

	def __init__(self, edges=set()):
		""" Initialize the object. 

		    If `edges` is passed, use a copy of `edges` for the object's edges attibute. 
		"""
		self.tagbuckets = {}
		self.edges = edges.copy()
	
	def as_pydot_graph(self):
		""" Return a copy of self as a pydot graph. """
		import pydot
		g = pydot.Dot()
		for edge in self.edges:
			g.add_edge(pydot.Edge(*edge))
		return g

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

	def has_edges(self, node1, *nodes):
		print node1, nodes
		pointer = node1
		for node in nodes:
			print self.matching((pointer, node))
			if not self.matching((pointer, node)):
				return False
			pointer = node
		return True

	def mutate(self, target, action = set.union):
		"""Add the edges of the `target` graph to `self` with the union set operation. If the action parameter is set, use a different set operation. 

		    Example:
		    >>> g1 = Graph(('a', 'b'))
		    >>> g2 = Graph(('c', 'd'))
		    >>> g1.mutate(g2)
		    >>> g1.edges
		    set(['a', 'c', 'b', 'd'])
		    """
		self.edges = action(self.edges, target.edges)

	def copy(self):
		""" Returns a copy of the object. """
		return Graph(self.edges)

	def tags(self):
		return self.tagbuckets.keys()

	def unique_num(self):
		"""Return a unique number. Currently returns a UUID based off the time. This should not be counted on. All you should count on is the number being unique and consisiting of letters and numbers."""
		return unique_num()

	def graph_with_tag(self, tag):
		return Graph(self.edges_with_tag(tag))

	def edges_with_tag(self, tag):
		try:
			return self.tagbuckets[tag]
		except KeyError:
			raise(TagError(tag))

	def add_tag(self, tag, first_node, *nodes):
		"""Like add, but it also tags the nodes."""
		first_node = self.specialize(first_node, tag=tag)
		ticker = first_node
		for i in nodes:
			self.__add(ticker,i, tag=tag)
			ticker = i	
		return first_node

	def add(self, first_node, *nodes):
		"""Create edges for each pair of nodes.

		    Example:
		    >>> g = Graph()
		    >>> g.add('a', 'b', 'c')
		    >>> g.edges
		    set([('a', 'b'), ('b', 'c')])
		    """
		return self.add_tag(None, first_node, *nodes)

	def specialize(self, a, tag=None):
		"""Internal method. It does the syntactical sugar. """
		if not isinstance(a, basestring):
			raise(TypeError("node is not a string"))
		nodes = a.split(".")
		node_o = self.__specialize(nodes.pop(0))
		node_holder = node_o
		for node in nodes:
			node = self.__specialize(node)
			self.__add(node_holder, node, tag=tag)
			node_holder = node
		return node_o

	def downwindedges(self,node, do_not_pass=set()):
		changed = True
		downwindedges = set()
		downwindnodes = set((node, ))
		while changed:
			changed = False
			for edge in self.edges:
				if (edge not in downwindedges
				    and edge[1] not in do_not_pass
				    and edge[0] in downwindnodes):
					changed = True
					downwindedges.add(edge)
					for n in edge:
						downwindnodes.add(n)
		return downwindedges

	def downwindgraph(self, node, do_not_pass=set()):
		return Graph(self.downwindedges(node, do_not_pass=do_not_pass))

	def edge_specialize(self, tag=None, *a):
		"""Specialize all edges in iterator `a`."""
		return tuple(self.specialize(b, tag=tag) for b in a)

	@property
	def nodes(self):
		"""Return all nodes in an object. This has to be generated on the fly and is not efficient.  

		    Example:
		    >>> g = Graph()
		    >>> g.add('a', 'b')
		    >>> g.nodes
		    set(['a', 'b'])
		    """
		return set(n for e in self.edges for n in e)

	def hasnode(self, n):
		"""Runs into the same efficiency problems as nodes. """
		return n in self.nodes

	def matching(self, e):
		"""Look for all edges matching `e`."""
		return [edge for edge in self.edges if match_edges(e, edge)]

	def replace(self, a, b):
		return Graph(set((tuple(b if node == a else node for node in edge) for edge in self.edges)))

	def query(self, q, loosen_anons=True):
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

		solutions = []
		if not isinstance(q, Graph):
			raise(TypeError("q is not a graph object", q))
		qes = q.edges
		if loosen_anons:
			qes = make_loose_matching(qes)
		self.__query(tuple(qes), solutions)
		return solutions

	def __add(self, a, b, tag=None):
		"""Internal function to add an edge with (`a`, `b`). """
		specialized = self.edge_specialize(tag, a,b)
		if tag is not None:
			try:
				tagbucket = self.tagbuckets[tag]
			except KeyError:
				tagbucket = set()
				self.tagbuckets[tag] = tagbucket
			tagbucket.add(specialized)
		self.edges.add(specialized)

	def add_info(self, more_info):
		more_info = more_info.copy()
		
		verbs = set(match['verb?'] for match in more_info.query(type_query("verb"))) 
	
		noun_query = type_query("noun")
		noun_query.add("action+lookup", "noun?")
	
	
		for match in more_info.query(noun_query):
			noun_graph = more_info.downwindgraph(match['noun?'], verbs)
			query = noun_graph.replace(match['noun?'], "noun?")
			for result in self.query(query):
				more_info = more_info.replace(match['noun?'], result["noun?"])
		self.mutate(more_info)	
		
	
	def __specialize(self, a, tag=None):
		"""Helper method for `graph.specialize`. """
		if a == "~":
			out = "~%s" % self.unique_num()
			# make the following DRY?
			self.__add(out, "anonymous+node", tag=tag)

		elif a == "" or a == "@":
			out = "@%s" % self.unique_num()
			self.__add(out, "anonymous+node", tag=tag)
		elif a == "*":
			out = "*%s" % self.unique_num()
		else:
			out = a
		self.last_specialized = out
		return out

	def __query(self, edges, solutions, solutionset = {}, consumed_edges = set()):
		""" Recursive internal query method. """

		if not edges:
			solutions.append(solutionset)
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
					self.__query(_edge_replace(edges, edge_, edge), solutions, solutionset, consumed_edges_c)

	""" File I/O. """
	def dump(self, f):
		""" Write the graph to a file-like object. """
		for e in self.edges:
			f.write("%s\t%s\n" % (e[0], e[1]))

	def load(self, f):
		""" Load the graph from a file-like object. """
		for line in f:
			self.add(*line.split("\t"))

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

def match_edges(edge1, edge2):
	r = tuple(match(n1, n2) for n1, n2 in zip(edge1,edge2)) 
	return r if r[0] and r[1] else False

def match(a,b):
	"""Return `b` if `b` matches `a`. Otherwise return `False`. 

	    For a match to be `True`, one of the following must be satisfied: 
		`a` == `b`
		`a` is a loose anonymous node and `b` is an anonymous node. 
		`a` contains "?"
		`a` contains "*"

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
	        or "*" in a
	        else False)

if __name__ == "__main__":
	a = Graph()
	b = Graph()
	a.add("a", "b")
	a.add_tag("tag", "a", "b")
	a.add_tag("tag", "b", "c")
	a.add_tag("tag2", "ad", "b")
	a.add_tag("tag2", "b", "cd")
	a.add("b", "d")
	b.add("?a", "b")
	b.add("b", "?c")

	from magicate import prettify
	for solset in a.graph_with_tag("tag2").query(b, True):
		print solset

def type_query(t):
	query = Graph()
	query.add(t+"?", "*1", t)
	query.add(t+"?", "anonymous+node")
	return query
