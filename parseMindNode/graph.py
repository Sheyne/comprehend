#! /usr/bin/env python
import uuid


class Map(object):
	def __init__(self):
		self.nodes = {}
	@property
	def contents(self):
		return [self.nodes[k] for k in self.nodes]
	
	def add(self, node, key = None):
		if key == None:
			key = uuid.uuid1()
		self.nodes[key] = node
		
	def get(self, key):
		return self.nodes[key]
	
	def matching(self, s):
		return [self.nodes[k] for k in self.nodes if str(self.nodes[k]) == str(s)]
	
	def starting_with(self, s):
		return [self.nodes[k] for k in self.nodes if str(self.nodes[k]).startswith(str(s))]

def match(q, t, anti_back = None):
	for edge in q.edges:
		if not anti_back or edge != anti_back:
			posible_matches = [e[0] for e in t.edges if e[1] == edge[1] and str(e[0]) == str(edge[0])]
			if not posible_matches:
				return False
			for node in posible_matches:
				if not match(edge[0], node, q.reciprocal_edge(edge)):
					return False
	return True

class Query(object):
	def __init__(self, map):
		self.map = map
		self.querynodes = self.map.starting_with("?")
		
	def match(self, dictionary):
		# rework to multiple, unknown querying. 
		query_node_count = len(self.querynodes)
		print query_node_count
		return [
					[dictionary.nodes[k]
						for k in dictionary.nodes
							if match(q,dictionary.nodes[k])]
				for q in self.querynodes]


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
