#! /usr/bin/env python
import uuid


class Node(object):
	"""API methods"""
	def match(self, target):
		return target if self.matchcmp(target) else None

	@property
	def value(self):
		return self.args[0] if len(self.args) == 1 else self.args

	def copy(self):
		return self.__class__(*self.args)

	"""Methods subclasses are encouraged to override. """
	def initialize(self): pass
	
	def matchcmp(self, target):
		return self == target
		
	def __eq__(self, target):
		return self.args == target.args

	@classmethod
	def claims(self, word):
		return True

	"""Internals"""	
		
	def __ne__(self, target):
		return not self == target

	def __init__(self, *args):
		self.args = args
		try:
			self.initialize(args)
		except TypeError:
			self.initialize()
	
	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, repr(self.value))
	
	@classmethod
	def node(self, *args):
		for sc in self.__subclasses__():
			node = sc.node(*args)
			if node:
				return node
		return self(*args) if self.claims(args[0]) else None
	
class AnonymousNode(Node):
	"""An anonymous node. It acts like a blank node, but is not equal to other blank nodes. """
	claim_string = ""
	def initialize(self):
		self.wild = False
	
	@classmethod
	def claims(self, word):
		return self.claim_string == word
		
	def __eq__(self, target):
		return id(self) == id(target)
	
	def wildcopy(self):
		c = self.copy()
		c.wild = True
		return c
	
	def matchcmp(self, target):
		try:
			return Node.__eq__(self, target) if (self.wild or target.wild) else self == target
		except AttributeError: # above will raise AttributeError if target is not an AnonymousNode
			return False

class TypeNode(AnonymousNode): 
	claim_string = "type"

class WildNode(AnonymousNode): 
	claim_string = "*"
	def matchcmp(self, target):
		return target

class QueryNode(WildNode): 
	def initialize(self, varnames):
		self.varnames = varnames
		try:
			self.varname = varnames[0]
		except IndexError: pass

	def __eq__(self, target):
		#allow for usage as dictionary keys
		return Node.__eq__(self, target)

	@classmethod
	def claims(self, word):
		return word.startswith("?")
	

class Map(object):
	"""
	A map contains a set of nodes, and a set of edges. 
	An edge is a tuple containing two nodes, a source and a target: `(source, target)`

	To link to nodes, call link and unlink on their map. """
	def __init__(self):
		"""Initialize map to default (empty) values. """
		self.nodes = set()
		self.edges = set()
		self.aliases = {}
		
	def link(self, a, *b):
		"""Link a to b, b to c, etc..."""
		for c in b:
			self.edges.add((a,c))
			a = c
	def unlink(self, a, *b):
		"""Unlink a from b, b from c, etc..."""
		for c in b:
			self.edges.remove((a,c))
			a = c
			
	def add(self, nodes, key = None):
		"""
		Add a node to the map. If the node contains a ".", process it as follows:
		convert dog.noun to:
		dog -> `TypeNode()` -> noun
		"""
		previous_node = None 
		for node in nodes.split("."):
			node = self.nodeadd(node)
			if previous_node:
				self.link(previous_node, self.nodeadd("type"), node)
			elif key:
				self.aliases[key] = node
			previous_node = node
		
	def get(self, key):
		"""If node was added with a "key", refer to that node. """
		return self.aliases[key]
	
	def matching(self, handler, *args):
		"""Return all nodes such that handler(node) is True."""
		return [node for node in self.nodes if handler(node, *args)]

	def nodeadd(self, node):
		"""Makes a new node object from node, adds it to self.nodes and returns it. """
		node = Node.node(node)
		self.nodes.add(node)
		return node

def match_edge(edge, dictionary, consumed_edges):
	"""Return a list of (edge, new edge) pairs. The new edge is the edge that is returned as a match from
	edge.match(edge). Neither match may result in None. """
	for de in dictionary.edges:
		a = (edge, (edge[0].match(de[0]), edge[1].match(de[1])))
		if a[1][0] and a[1][1] and not a[1] in consumed_edges:
			yield a

def tuple_replace(source, old, new):
	return tuple(new if a == old else a for a in source)

def edge_replace(source, old_edge, new_edge):
	"""Convert old_edge[a] to new_edge[a] in source. """
	res = source
	for replace_pair in zip(old_edge, new_edge):
		res = tuple_replace(res, *replace_pair)
	return res

def match_edges(dictionary, edge, edge_list, consumed_edges):
	"""Take an edge and look through the dictionary for posible matches. 
	Copy edge_list and store the results of the match in it. yield every posible edge_list. """
	for old_edge, new_edge in match_edge(edge, dictionary, consumed_edges):
		yield new_edge, [edge_replace(source, old_edge, new_edge) for source in edge_list]

def wildize_anonymi(edge_list):
	return [tuple(n.wildcopy() if isinstance(n, AnonymousNode) else n for n in edge) for edge in edge_list]

class Query(object):
	"""Initialize query to default values and add the map. """
	def __init__(self, map):
		self.map = map
		self.querynodes = self.map.matching(isinstance,QueryNode)
		
	def match(self, dictionary):
		self.solutions = []
		edge_list = wildize_anonymi(self.map.edges)
		self.rmatch(edge_list, dictionary)
		return self.solutions
		
	def rmatch(self, edge_list, dictionary, query_matches = {}, consumed_edges = set(), indent = ' '):
		query_matches = query_matches.copy()
		consumed_edges = consumed_edges.copy()
		print indent, "edge list", edge_list
		if not edge_list:
			print indent, "Made it to depth", query_matches
			self.solutions.append(query_matches)
			return True
		working_edge = edge_list.pop()
		print indent,"working with edge", working_edge
		for new_working_edge, ps in match_edges(dictionary, working_edge, edge_list, consumed_edges):
			consumed_edges.add(new_working_edge)
			for old_node, new_node in zip(working_edge, new_working_edge):
				if isinstance(old_node, QueryNode):
					print indent, 
					"wow pro working edge", working_edge, new_working_edge
					
					query_matches[old_node] = new_node
			print indent, "posible solution:",ps
			self.rmatch(ps, dictionary, query_matches,consumed_edges, indent = indent + "  ")