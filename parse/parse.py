#! /usr/bin/env python

import graph
import mindnode

# load a graph from a mindnode type graph
dictionary = mindnode.mindmap('dictionary.mindnode')

# dump the graph into 'dictionary.edgepairgraph'
dictionary.dump(open("dictionary.edgepairgraph","w"))

# load another graph from a mindnode type graph. 
enviroment = mindnode.mindmap('enviroment.mindnode')

# merge dictionary into the enviroment
enviroment.union(dictionary)

# load another graph from a mindnode type graph. 
query_dictionary = mindnode.mindmap('queries/test1.mindnode')
# this graph will be used as a query. 

# run the query on the envieroment
for result in enviroment.query(query_dictionary):
	# print out result dictionaries. 
	print result