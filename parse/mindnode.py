import plistlib
import zipfile
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from cStringIO import StringIO
import graph


def unrtf(value):
	return PlaintextWriter.write(Rtf15Reader.read(StringIO(value))).getvalue()

class MindMap(graph.Map):
	def __init__(self, filename):
		super(self.__class__, self).__init__()
		with zipfile.ZipFile(filename, 'r') as z:
			with z.open('contents.xml') as contents:
				dom = plistlib.readPlist(contents)
				map = dom['mindMap']
				for node in map['mainNodes']:
					value = unrtf(node['title']['text'])
					id = node['nodeID']
					self.add(value, id)
				
				for association in map['associations']:
					s = self.get(association['startNodeID'])
					e = self.get(association['endNodeID'])
					self.link(s,e)
