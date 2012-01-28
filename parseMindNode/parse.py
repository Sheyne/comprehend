import plistlib
import zipfile
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from cStringIO import StringIO



def unrtf(value):
	return PlaintextWriter.write(Rtf15Reader.read(StringIO(value))).getvalue()

from query.graph import Node


def load_map(f):
	nodes = {}
	with zipfile.ZipFile(f, 'r') as z:
		with z.open('contents.xml') as contents:
			dom = plistlib.readPlist(contents)
			map = dom['mindMap']
			for node in map['mainNodes']:
				value = unrtf(node['title']['text'])
				id = node['nodeID']
				nodes[id] = Node(value)
			
			for association in map['associations']:
				s = nodes[association['startNodeID']]
				e = nodes[association['endNodeID']]
				s.point_at(e)
	return nodes


dictionary = load_map('dictionary.mindnode')
query_map = load_map('query.mindnode')

querys = [query_map[key] for key in query_map if str(query_map[key]) == "?"]

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
	
def query(q, dictionary):
	return [dictionary[k] for k in dictionary if match(q,dictionary[k])]
			
for q in querys:
	print query(q, dictionary)
