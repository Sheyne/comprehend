# Graphical Sentence Modeling for Computerized Interpretation of Natural Language 

## Goal

The project's goal is to create an Information Retrieval System (IRS). The IRS will parse English sentences and build a model. This model can be easily added to a database of learned information, or used to query an existing database. 

## Procedure

1. The project must be able to simply model natural language.
2. The project must be able to use this model to better interpret natural language documents. 

## Modeling 

### Graphs
To model a sentence, I am using a directed graph. Graphs are a type of structure that consist of a set of "nodes". These nodes are connected by "edges". In a visual representation, nodes are points, and the edges that connect them are lines or curves. This can be seen visually in Figure 1. In a directed graph, edges have a direction associated to them--from one node to another. 

![Figure 1](http://dl.dropbox.com/u/3030738/Screenshots/a%20directed%20graph.png) 

***Figure 1**: the dashed blue arrows are edges, and the grey rectangles are nodes.* 
___

### Modeling Method
To model a sentence, I represent each word as node and add edges between these nodes to give the sentence meaning. This can be seen in Figure 2. 

![Figure 2](http://dl.dropbox.com/u/3030738/Screenshots/simple%20language%20graph%20example.png)

***Figure 2**: here we have words connected by edges to give meaning.* 
___

#### Nouns
When we talk about a specific object, such as a dog, we refer to it as "the dog". We are not talking about the word "dog", but about a specific object that is a dog. To model this, we make a new node and add an edge that points at the "dog" node. These nodes are called anonymous nodes. We use an `@` sign followed by a unique id to represent an anymous node to simplify referencing it. 

![Figure 3](http://dl.dropbox.com/u/3030738/Screenshots/r4iztwx_xu06.png)

***Figure 3**: here we show an example of an anonymous node. `@1` represents the dog instance.*
___

#### Other Anonymous Nodes
The idium of using a blank node that has an edge pointing at at anonther word to define it is common throughout the model. It is used for nouns instances, verb instances, and adverb instances. This allows us to define how the verb was performed, or add adverbial phrases. All of the phemonena can be seen in Figure 3. 

![Figure 4](http://dl.dropbox.com/u/3030738/Screenshots/yxg2v~5gz_4q.png)

***Figure 4**: is generated by the sentence: "The dog runs around the block."*
___
In the figure, `@1` represents an instance of the noun "dog", `@2` an instance of the verb "run", `@3` is an instance of the adverb "around", and `@4` is an instance of the noun "block".

Figure 3 indicates that it would be convenient to store some definitions that will always be true--such as `dog -> noun`--in a dictionary.

This introduces some new terminology, an *enviroment* stores specific information, such as a story about a dog, while a *dictionary* holds information that will always be true, such as the properties of the english language. 

#### Question Modeling
The model of a question takes a similar form to the model of a statement. The difference is that one or more of the nodes in a question graph are marked as unknown.

## Retrieval
We can take model of a question and "query" it on a sentence model. The process takes the edges of the question model looks for matches to them in the enviroment (knowledge) model. This allows the program to fill in the unknowns in the query, and return a result. 

	Here I'll add an explination of the internal query algorithm.