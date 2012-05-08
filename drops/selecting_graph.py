class Node(object):
	def __init__(self, graph, left_restrictions=set(), right_restrictions=set()):
		self.graph = graph
		self.left_restrictions = left_restrictions.copy()
		self.right_restrictions = right_restrictions.copy()
	
	def restrict_left(self, restriction):
		self.left_restrictions.add(restriction)

	def restrict_right(self, restriction):
		self.right_restrictions.add(restriction)
	
	def possibilities(self):
		g = self.graph
		return g.havingrights(self.right_restrictions) & g.havinglefts(self.left_restrictions)
		
class Graph(object):
	def __init__(self, base=None):
		"""	The graph class is highly optimized for assignments and lookups, but it a
			memory hog; it uses ~300% the memory an optimum version would. """
		if base is not None:
			self.edges = base.edges.copy()
			self.edges_l = base.edges_l.copy()
			self.edges_r = base.edges_r.copy()
		else:
			self.edges = set()
			self.edges_l = {}
			self.edges_r = {}
		
	def add_edge(self, *nodes):
		i = iter(nodes)
		l = next(i)
		for r in i:
			self.edges.add((l,r))
			self.havingleft(l).add(r)
			self.havingright(r).add(l)
			l = r

	def having(self, node, d):
		try:
			return d[node]
		except KeyError:
			bucket = set()
			d[node] = bucket
			return bucket	

	def hasedge(self, edge):
		return edge in self.edges
	
	def havings(self, nodes, havingfunc):
		i = iter(nodes)
		try:
			a = havingfunc(next(i))
		except StopIteration:
			return self.nodes()
		else:
			for b in i:
				a &= havingfunc(b)
			else:
				return a
			return a

	def havinglefts(self, nodes):
		return self.havings(nodes, self.havingleft)

	def havingleft(self, node):
		return self.having(node, self.edges_l)

	def havingrights(self, nodes):
		return self.havings(nodes, self.havingright)
	
	def havingright(self, node):
		return self.having(node, self.edges_r)

	def enumerate_edges(self):
		return (e for e in self.edges)
	
	def nodes(self):
		return {x for y in self.edges for x in y}
	
	def node(self, left_restrictions=set(), right_restrictions=set()):
		return Node(self, left_restrictions, right_restrictions)
		

g = Graph()
g.add_edge('a', 'b', 'c')
g.add_edge('a', 'd')
print(g.node({'a'}, {'c'}).possibilities())