#! /usr/bin/env python

import graph
import mindnode
import sys
import os
from datetime import datetime

print """Begining Processing:
date of start: %s

""" % (datetime.now(), )

dictionary = mindnode.MindMap(os.path.expanduser('dictionary.mindnode'))

enviroment = mindnode.MindMap(os.path.expanduser('enviroment.mindnode'))

enviroment.load(dictionary)

queryname = os.path.expanduser('queries/test1.mindnode')

query_dictionary = mindnode.MindMap(queryname)

for result in enviroment.query(query_dictionary):
	print result