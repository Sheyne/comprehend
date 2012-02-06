import uuid


def node_replace(node, old, new):
	for old_n, new_n in zip(old, new):
		if old_n == node:
			return new_n
	return node

def nodes_replace(edge, old, new):
	return tuple(node_replace(node, old, new) for node in edge)

def edge_replace(edges, old, new):
	return tuple(nodes_replace(edge, old, new) for edge in edges)

def dasherize(edges):
	return set(tuple(n.replace("_", "-") for n in edge) for edge in edges)
	
def match(a,b):
	if a == b:
		return b
	a_ = a.split("-")
	b_ = tuple(x for y in b.split("_") for x in y.split("-"))
	return "_".join(b_) if a_[0] == b_[0] or a_[0] == "*" or a_[0].startswith("?") else False

def match_edges(edge1, edge2):
	r = tuple(match(n1, n2) for n1, n2 in zip(edge1,edge2)) 
	return r if r[0] and r[1] else False

class graph(object):
	def __init__(self, edges = set()):
		self.edges = edges.copy()
	
	def combine(self, target, action = set.union):
		return graph(action(self.edges, target.edges))
	
	def load(self, target, action = set.union):
		self.edges = action(self.edges, target.edges)
	
	def unique_num(self):
		return uuid.uuid4()

	def _add(self, a, b):
		self.edges.add(self.edge_specialize(a,b))
	
	def add(self, *nodes):
		nodes = list(nodes)
		a = nodes.pop(0)
		for i in nodes:
			self._add(a,i)
			a = i

	def specialize(self, a):
		nodes = a.split(".")
		node_o = self._specialize(nodes.pop(0))
		node_holder = node_o
		for node in nodes:
			node = self._specialize(node)
			t = self._specialize("type")
			self._add(node_holder, t)
			self._add(t, node)
			node_holder = node
		return node_o
		
	def _specialize(self, a):
		if a == "":
			out = "_%s" % self.unique_num()
		elif a == "type":
			out = "type_%s" % self.unique_num()
		else:
			out = a
		self.last_specialized = out
		return out
		
	def edge_specialize(self, *a):
		return tuple(self.specialize(b) for b in a)
	
	@property
	def nodes(self):
		return set(n for e in self.edges for n in e)
	
	def matching(self, e):
		return [edge for edge in self.edges if match_edges(e, edge)]

	def query(self, q):
		self.solutions = []
		
		self._query(tuple(dasherize(q.edges)))
		return self.solutions
	
	def _query(self, edges, solutionset = {}, consumed_edges = set()):
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
						if key.startswith("?"):
							solutionset[key] = value
					self._query(edge_replace(edges, edge_, edge), solutionset, consumed_edges_c)