# Graphical Sentence Modeling for Computerized Interpretation of Natural Language 

## Goal

The project's goal is to create an Information Retrieval System (IRS). The IRS will parse English sentences and build a model. This model can be easily added to a database of learned information, or used to query an existing database. 

## Specifications

The project must be able to model english sentences, and retrieve information from those models. 

## Modeling 

### Graphs
To model a sentence, I am using a directed graph. Graphs are a type of structure that consist of a set of "nodes". These nodes are connected by "edges". In a visual representation, nodes are points, and the edges that connect them are lines or curves. This can be seen visually in Figure 1. In a directed graph, edges have a direction associated to them--from one node to another. 

### Modeling Method
To model a sentence, I represent each word as node and add edges between these nodes to give the sentence meaning. This can be seen in Figure 2. 

#### Nouns
When we talk about a specific object, such as a dog, we refer to it as "the dog". We are not talking about the word "dog", but about a specific object that is a dog. To model this, we make an empty node and add an edge that points at the "dog" node. 

#### Other Blank Nodes
The idium of using a blank node that has an edge pointing at at anonther word to define it is common throughout the model. It is used for nouns instances, verb instances, and adverb instances. This allows us to define how the verb was performed, or add adverbial phrases. 

#### Question Modeling
The model of a question takes a similar form to the model of a statement. The difference is that one or more of the nodes in a question graph are marked as unknown.

## Retrieval
We can take model of a question and "query" it on a sentence model. The process takes the edges of the question model looks for matches to them in the enviroment (knowledge) model. This allows the program to fill in the unknowns in the query, and return a result. 


# Figures
1. basic graph -> http://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/6n-graf.svg/200px-6n-graf.svg.png
2. basic sentence graph. Render a graph of `(dog noun, ball noun, chase verb)`