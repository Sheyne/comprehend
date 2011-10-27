# Links

## Introduction

The fundamental element of the data structure is the link. A link consists of a source node pointing a label node at a target node. 

Link structure: `{source} -- {label} -> {target}`

For usage of this structure in english, both the source and target are nouns, and the label is a verb: (`{doer:noun} -- {action:verb} -> {doee:noun}`). It is posible to convert any sentence into this form. --DISCUSS ADJECTIVES--

Example: "The dog is red." becomes: `[dog] -- is -> red`

The brackets around dog imply the bracketed object is an instance of `dog`. This is because all nodes are instances of objects, ie. proper nouns; this says that an object of type dog is red. If we said that sam is a dog. Then sam is red. The structure would look like: 

	Sam -- type -> dog
	|
    is -> red

Internally `[dog] -- is -> red` becomes:

	# -- type -> dog
	|
    is -> red

The brackets are just a shorthand.

### Unknown targets

A for some sentences, the target is undefined. For example: "The dog chases", translates to: `[dog] -- chases -> #`. We are unsure of what the dog is chasing. `#` represents an unknown quantity.

## Queries

Suppose the initial knowledge is: "The dog chases the cat. ", we build the structure: `[dog] -- chases -> [cat]`. 

The benefit to storing data in this structure is that we can easily query information from the structure. We can query the structure with questions. For example "What does the dog chase?". This becomes `[dog] -- chases -> ?`. If the query was run on the above, `?` would equal `[cat]`. This introduces the `?` token; `?` is like `#` except that `#` represents unknown data, and `?` represents desired data. 