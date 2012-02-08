import plistlib
import zipfile
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from cStringIO import StringIO
import graph


def unrtf(value):
	return PlaintextWriter.write(Rtf15Reader.read(StringIO(value))).getvalue()

def mindmap(filename):
	g = graph.graph()
	with zipfile.ZipFile(filename, 'r') as z:
		with z.open('contents.xml') as contents:
			dom = plistlib.readPlist(contents)
			map = dom['mindMap']
			
			relations = {}
			
			for node in map['mainNodes']:
				value = unrtf(node['title']['text'])
				id = node['nodeID']
				relations[id] = g.specialize(value)
				relations[id+"_"] = g.last_specialized
	
			for association in map['associations']:
				suffix = "_" if association["startArrow"] == 4 else ""
				s = relations[association['startNodeID']+suffix]
				e = relations[association['endNodeID']]
				g.add(s,e)

	return g
