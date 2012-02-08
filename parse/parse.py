#! /usr/bin/env python

import graph
import mindnode
import sys
import os
from datetime import datetime

dictionary = mindnode.mindmap(os.path.expanduser('dictionary.mindnode'))

dictionary.dump(open("dictionary.comprehenddictionary","w"))

enviroment = mindnode.mindmap(os.path.expanduser('enviroment.mindnode'))
enviroment.union(dictionary)

query_dictionary = mindnode.mindmap(os.path.expanduser('queries/test1.mindnode'))

for result in enviroment.query(query_dictionary):
	print result