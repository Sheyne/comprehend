## Node
An entity in the graph. 

## Word
A word is a node. It is represented by a string of letters, numbers and underscores. All words represent the same thing throughout a graph. 

## Connection (Edge)
A connection is a pair of nodes, where the first "points" at the second. It is represented by two words enclosed in parentheses. i.e. `(a b)` creates an edge from a to b. 

## Graph
A graph is a set of edges. Graphs can have a name, which must be a word prefixed by `&`. Graphs themselves can be used as nodes, and because of this can be pointed at by edges. 

