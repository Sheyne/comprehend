#! /usr/bin/env python

import graph
import mindnode
import sys
import os
from datetime import datetime

dictionary = mindnode.MindMap(os.path.expanduser('dictionary.mindnode'))

queryname = os.path.expanduser('queries/test1.mindnode')

query = graph.Query(mindnode.MindMap(queryname))

print """Begining Processing:
date of start: %s

""" % (datetime.now(), )

print "dictionary.edges:", dictionary.edges

a = graph.Node.node("hi")
b = graph.Node.node("you")
c = graph.Node.node("are")
c = graph.Node.node("test")
d = graph.Node.node("1")


for solution in query.match(dictionary):
	print "A solution"
	for key in solution:
		print key, repr(solution[key])
		print [edge for edge in dictionary.edges if edge[0] == solution[key]]