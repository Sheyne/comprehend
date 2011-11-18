class LinkNotFound(KeyError): pass

class Node(object):
	links = set()
	def __init__(self, tag):
		self.tag = tag
	
	def __str__(self):
		return self.tag
	
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, repr(self.tag))
	
	def link_to(self, action = None, target = None)
		Link(self, action, target)
	
	def add_link(self, link)
		self.links.add(link)
	
	def remove_link(self, link)
		try:
			self.links.remove(link)
		except KeyError:
			raise(LinkNotFound("Cannot remove link: the link was not found."))

class Mark(Node):
	pass

def hash_if_none(node):
	if node == None:
		return Mark("#")
	return node


class Link(object):
	def __init__(self, source = None, action = None, target = None):
		if not (source == None and action == None and target == None):
			self.source = hash_if_none(source)
			self.action = hash_if_none(action)
			self.target = hash_if_none(target)
			self.source.add_link(self)
			self.target.add_link(self)			
	
	def destroy(self):
		self.source.remove_link(self)
		self.target.remove_link(self)			
	
	def __del__(self):
		self.destroy()
	
	def __str__(self):
		return "%s -- %s -> %s" % (self.source, self.action, self.target)
	

def mainloop():
		

if __name__==""



