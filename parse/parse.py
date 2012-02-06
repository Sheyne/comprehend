#! /usr/bin/env python

import graph
import mindnode
import sys
import os
from datetime import datetime

dictionary = mindnode.MindMap(os.path.expanduser('dictionary.mindnode'))

queryname = os.path.expanduser('queries/test1.mindnode')

query_dictionary = mindnode.MindMap(queryname)

print """Begining Processing:
date of start: %s

""" % (datetime.now(), )

for result in dictionary.query(query_dictionary):
	print result