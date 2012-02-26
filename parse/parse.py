#! /usr/bin/env python

import graph
import graph.mindnode

def main():
    # load a graph from a mindnode type graph
    dictionary = graph.mindnode.mindmap('resources/dictionary.mindnode')

    # dump the graph into 'dictionary.edgepairgraph'
    dictionary.dump(open("resources/dictionary.edgepairgraph","w"))

    # load another graph from a mindnode type graph. 
    enviroment = graph.mindnode.mindmap('resources/enviroment.mindnode')

    # merge dictionary into the enviroment
    enviroment.union(dictionary)

    # load another graph from a mindnode type graph. 
    query_dictionary = graph.mindnode.mindmap('resources/queries/test1.mindnode')
    # this graph will be used as a query. 

    # run the query on the envieroment
    for result in enviroment.query(query_dictionary):
        # print out result dictionaries. 
        print result


if __name__ == "__main__":
    # jump into the dir of the script (xcode launches from some wierd place). 
    import os
    os.chdir(os.path.dirname(__file__))
    main()
