#! /usr/bin/env python
import uuid

class AnonymousNode(object):
	"""An anonymous node. It acts like a blank node, but is not equal to other blank nodes. """
	def __str__(self):
		return "#"
	
class TypeNode(AnonymousNode):
	"""Type node. It is like a normal node with value "type", except that it is not equal to other "type" nodes. TypeNodes are used to avoid type -> type -> type -> ect...."""
	def __str__(self):
		return "type"

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
		
	def link(self, a, *b):z
		"""Link a to b, b to c, etc.."""
		for c in b:
			self.edges.add((a,c))
			a = c
	def unlink(self, a, *b):
		"""Unlink a from b, b from c, etc.."""
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
				tn = self.nodeadd("type")
				self.link(pn, tn)
				self.link(tn, node)
			elif key:
				self.aliases[key] = node
				key = None
		
	def get(self, key):
		"""If node was added with a "key", refer to that node. """
		return self.aliases[key]
	
	def matching(self, handler):
		"""Return all nodes such that handler(node) is True."""
		return [node for node in self.nodes if handler(node)]

	def nodeadd(self, node):
		"""The interal function that actually adds the node. It returns the node, as it may change it's value. This would happen if the node is blank--becomes anonymous--or if it is "type"--becomes a TypeNode. """
		if nodes == "":
			a = AnonymousNode()
			self.nodes.add(a)
			return a
		elif nodes == "type":
			a = TypeNode()
			self.nodes.add(a)
			return a
		else:
			self.nodes.add(node)
			return node
	
class Query(object):
	"""Initialize query to default values and add the map. """
	def __init__(self, map):
		self.map = map
		self.querynodes = self.map.starting_with("?")
		
	def match(self, dictionary):
		for edge in self.map.edges:
			"""TODO: Add a compare function that allows for wildcards, and for Anonymous nodes to equal each other. """
			print edge
