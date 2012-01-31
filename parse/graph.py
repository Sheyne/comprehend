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

class LooseAnonymousNode(AnonymousNode): pass
class LockedAnonymousNode(AnonymousNode): pass

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
		
	def get(self, key):
		"""If node was added with a "key", refer to that node. """
		return self.aliases[key]
	
	def matching(self, handler, *args):
		"""Return all nodes such that handler(node) is True."""
		return [node for node in self.nodes if handler(node, *args)]

	def matching_edges(self, handler, *args):
		return matching_edges(handler, self.edges, *args)

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
	return (
		isinstance(a, WildNode) or
		isinstance(b, WildNode) or
		(isinstance(a, TypeNode) and isinstance(b, TypeNode)) or
		(isinstance(a, AnonymousNode) and isinstance(b, LooseAnonymousNode)) or
		a == b
	)

def compare_edges(a,b, *args):
	return compare_nodes(a[0],b[0],*args) and compare_nodes(a[1],b[1],*args)

def copy_attrs(source, target):
	target.__dict__.update(source.__dict__)
	return target

def replace_class(l, t1, t2, strict = False):
	cmp_fun = (lambda a,b: a.__class__ == b) if strict else isinstance
	return [tuple(
				copy_attrs(n, t2()) if cmp_fun(n, t1) else n for n in e
			) for e in l]

def replace_node(l, n1, n2):
	return [tuple(n2 if n1 == n else n for n in e) for e in l]


class Query(object):
	"""Initialize query to default values and add the map. """
	def __init__(self, map):
		self.map = map
		self.querynodes = self.map.matching(isinstance,QueryNode)
		
	def match(self, dictionary):
		self.solutions = []
		edge_list = replace_class(self.map.edges, AnonymousNode, LooseAnonymousNode, strict = True)
		self.rmatch(edge_list, dictionary)
		return self.solutions
		
	def rmatch(self, edge_list, dictionary, query_matches = {}, indent = ' '):
		query_matches = query_matches.copy()
		if not edge_list:
			print indent, "Made it to depth"
			self.solutions.append(query_matches)
			return True
		working_edge = edge_list.pop()
		print "\n",indent, "Working edge:",working_edge
		for posible_solution in dictionary.matching_edges(compare_edges,working_edge):
			print indent, "posible solution:",posible_solution
			wel = edge_list #working edge list
			for pos in range(2):
				node = working_edge[pos]
				if isinstance(node, LooseAnonymousNode) or isinstance(node, QueryNode) or isinstance(node, TypeNode):
					wel = replace_node(wel, node, posible_solution[pos])
					if isinstance(node, QueryNode):
						print indent, "Posible query answer for %s is %s" % (node.var, posible_solution[pos])
						query_matches[node.var] = posible_solution[pos]
			self.rmatch(wel, dictionary, query_matches, indent = indent+'  ')