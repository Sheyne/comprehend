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

for solution in query.match(dictionary):
	print "the real solution is:",solution


a = graph.AnonymousNode()
b = graph.LooseAnonymousNode()
c = graph.AnonymousNode()

l = [(a, "hi"), ("hi", b)]

l2 = graph.replace_node(l, b, c)
print "printing l2"
print l2

print "printing 1"
print graph.matching_edges(graph.compare_edges,l,("hi",b))
print "printing 2"
print graph.matching_edges(graph.compare_edges,l2,("hi",b))

