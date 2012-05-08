from glob import iglob as glob
#from pydot import Graph, Edge
import pydot

examples = {}

anoncounter = 0

for path in glob("*.md"):
	with open(path, 'r') as f:
		name = None
		for line in f:
			if line.startswith('Example '):
				name = 'example.'+line.strip()[8:-1]
				examples[name] = pydot.Dot(name, graph_type='digraph')
			elif name is not None:
				if line.startswith('\t'):
					graph = examples[name]
					lst = None
					for node in line.split('->'):
						node = node.strip()
						if node.endswith("'"):
							n = "@"+str(anoncounter)
							anoncounter += 1
							graph.add_edge(pydot.Edge(n, node[:-1]))
							node = n
						if lst is not None:
							graph.add_edge(pydot.Edge(lst, node))
						lst = node
				else:
					name = None

for key, g in examples.items():
	g.write(key+'.png', format='png')