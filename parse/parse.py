#! /usr/bin/env python

import graph
import mindnode

def main():
    # load a graph from a mindnode type graph
    dictionary = mindnode.mindmap('resources/dictionary.mindnode')

    # dump the graph into 'dictionary.edgepairgraph'
    dictionary.dump(open("resources/dictionary.edgepairgraph","w"))

    # load another graph from a mindnode type graph. 
    enviroment = mindnode.mindmap('resources/enviroment.mindnode')

    # merge dictionary into the enviroment
    enviroment.union(dictionary)

    # load another graph from a mindnode type graph. 
    query_dictionary = mindnode.mindmap('resources/queries/test1.mindnode')
    # this graph will be used as a query. 

    # run the query on the envieroment
    keep_it_up = True
    for result in enviroment.query(query_dictionary):
        # print out result dictionaries. 
        for key in result:
            print "%s is %s." % ((key.replace("?", "") or "Your answer"), result[key])
        keep_it_up = False
    if keep_it_up:
        print "No results found. "


if __name__ == "__main__":
    # jump into the dir of the script (xcode launches from some wierd place). 
    import os
    os.chdir(os.path.dirname(__file__))
    main()
