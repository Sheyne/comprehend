#! /usr/bin/env python

import graph
import mindnode
import sys

dictionary = mindnode.MindMap('dictionary.mindnode')

queryname = 'queries/%s.mindnode' % sys.argv[1]

query = graph.Query(mindnode.MindMap(queryname))

print query.match(dictionary)