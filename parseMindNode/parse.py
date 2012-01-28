import graph
import mindnode

dictionary = mindnode.MindMap('dictionary.mindnode')
query = graph.Query(mindnode.MindMap('query.mindnode'))

print query.match(dictionary)