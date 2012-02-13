import plistlib
import zipfile
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from cStringIO import StringIO
import graph
import os


def unrtf(value):
	return PlaintextWriter.write(Rtf15Reader.read(StringIO(value))).getvalue()

def rertf(value):
	return Rtf15Writer.write(value).getvalue()


def readMindMap(filename):
	with zipfile.ZipFile(filename, 'r') as z:
		with z.open('contents.xml') as contents:
			return plistlib.readPlist(contents)

def writeMindMap(data, filename):
	with zipfile.ZipFile(filename, 'w') as z:
		z.writestr("contents.xml", plistlib.writePlistToString(data))

def simpleMainNode(node):
	return {
	"contentAlignment": 1,
	"fillColor":"{1.000, 1.000, 1.000, 1.000}",
	"isDecreasingBranchThickness":True,
	"isDrawingFill": True,
	"isLeftAligned": False,
	"location": "{-440.9384765625, 45.5}",
	"nodeID": node,
	"strokeColor": "{0.500, 0.500, 0.500, 1.000}",
	"strokeStyle": 0,
	"strokeWidth": 2,
	"subnodes": [],
	"title":
		{
		"constrainedWidth": 300,
		"shrinkToFitContent": 1,
		"text": node,
		},
	}

def simpleAssociation(node1, node2):
	return {
		"endArrow": 2,
		"endNodeID": node2,
		"startArrow": 0,
		"startNodeID": node1,
		"strokeColor": "{0.000, 0.500, 1.000, 1.000}",
		"strokeStyle": 3,
		"strokeWidth": 1, 
		"wayPointOffset": "{45.0352, 49.2559}",
	}

def mindmap(filename):
	g = graph.graph()
	map = readMindMap(filename)['mindMap']
	
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

def write(graph, filename):
	map = readMindMap(os.path.join(os.path.dirname(__file__), "empty.mindnode"))['mindMap']
	
	map['mainNodes'] = [simpleMainNode(n) for n in graph.nodes]
	
	map['associations'] = [simpleAssociation(n1, n2) for n1, n2 in graph.edges]
	
	writeMindMap(map, filename)