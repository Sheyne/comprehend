#! /usr/bin/env python
import uuid

class AnonymousNode(object):
	def __str__(self):
		return "#"
	
class TypeNode(AnonymousNode):
	def __str__(self):
		return "type"

class Map(object):
	"""Nodes are now simple strings, except for two special cases: anonymous nodes, which act like blanks, and type nodes, which act like "type" but do not equal each other. 

		A map contains a set of nodes, and a set of edges. All links are in the edges. 

		To link to nodes, call link and unlink on their map. 

		Read the description of the add function for the new modifications to the design"""
	def __init__(self):
		self.nodes = set()
		self.edges = set()
		self.aliases = {}
		
	def link(self, a, b):
		self.edges.add((a,b))
	def unlink(self, a, b):
		self.edges.remove((a,b))
	@property
	def contents(self):
		return [self.nodes[k] for k in self.nodes]
	
	def nodeadd(self, node):
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
	
	def add(self, nodes, key = None):
		"""
		Add a node to the map. If the node contains a ".", process it as follows:
		convert dog.noun to:
		dog -> `TypeNode()` -> noun
		
		TypeNodes are used to avoid type -> type -> type -> ect....
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
		return self.aliases[key]
	
	def matching(self, s):
		return [self.nodes[k] for k in self.nodes if str(self.nodes[k]) == str(s)]
	
	def starting_with(self, s):
		return [k for k in self.nodes if str(k).startswith(str(s))]

class Query(object):
	def __init__(self, map):
		self.map = map
		self.querynodes = self.map.starting_with("?")
		
	def match(self, dictionary):
		for edge in self.map.edges:
			"""
			add a compare function that allows for wildcards, and for Anonymous nodes to equal each other. 
			"""
			print edge
