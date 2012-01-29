#! /usr/bin/env python
import uuid


class AnonymousNode(object):
	uniq = 0
	"""An anonymous node. It acts like a blank node, but is not equal to other blank nodes. """
	def __init__(self, *args):
		self.args = args
		self.uniq = AnonymousNode.uniq
		AnonymousNode.uniq+=1
	def __str__(self):
		return "."
	
class TypeNode(AnonymousNode):
	"""Type node. It is like a normal node with value "type", except that it is not equal to other "type" nodes. TypeNodes are used to avoid type -> type -> type -> ect...."""
	def __str__(self):
		return "type"
class WildNode(AnonymousNode):
	def __str__(self):
		return "*"
class QueryNode(WildNode):
	def __init__(self, var):
		self.var = var
	def __str__(self):
		return "?"

special_nodes = {
	"": (AnonymousNode, str.__eq__),
	"type": (TypeNode, str.__eq__),
	"?": (QueryNode, str.startswith),
	"*": (WildNode, str.__eq__),
}


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
				key = None
			previous_node = node
	
	def matching_edges(self, handler, *args):
		return matching_edges(handler, self.edges, *args)
	
	def get(self, key):
		"""If node was added with a "key", refer to that node. """
		return self.aliases[key]
	
	def matching(self, handler, *args):
		"""Return all nodes such that handler(node) is True."""
		return [node for node in self.nodes if handler(node, *args)]

	def nodeadd(self, node):
		"""The interal function that actually adds the node. It returns the node, as it may change it's value. This would happen if the node is blank--becomes anonymous--or if it is "type"--becomes a TypeNode. """
		for k in special_nodes:
			if special_nodes[k][1](node, k):
				a = special_nodes[k][0](node)
				self.nodes.add(a)
				return a
		else:
			self.nodes.add(node)
			return node

def matching_edges(handler,edges, *args):
	return [edge for edge in edges if handler(edge, *args)]

def compare_nodes(a,b):
	return isinstance(a, WildNode) or isinstance(b, WildNode) or str(a) == str(b)

def compare_edges(a,b):
	return compare_nodes(a[0],b[0]) and compare_nodes(a[1],b[1])

class Query(object):
	"""Initialize query to default values and add the map. """
	def __init__(self, map):
		self.map = map
		self.querynodes = self.map.matching(isinstance,QueryNode)
		
	def match(self, dictionary):
		edge = self.map.edges.__iter__().next() # get any random edge
		return self.rmatch(edge, self.map.edges, dictionary.edges)
		
	def rmatch(self, edge, m_edges, d_edges):
		#print "aaaaaaaaa", edge, "bbbbbbbbb", m_edges, "ccccccccc", d_edges
		matches = matching_edges(compare_edges, d_edges, edge)
		if matches:
			for match in matches:
				n_edges = m_edges.copy()
				n_edges 
				print match
		else:
			return False