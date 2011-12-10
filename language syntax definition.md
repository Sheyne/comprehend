# Dictionary Rules

`a`: **word**--constant and global. (Technically a **global word**)

`[a]`: **scoped word**--can be used anywhere that a word could, but they have the benefit of scoping (`[b]` in one scope is not equal `[b]` in another scope).

`a<x>`: **word scan order**--scan the sentence for the word and plug in. The words need to be found in the sentence in the correct scan order. 

`#`: **anonymous word**--a each `#` is a unique word with no tag name.

`a b c`:linkage--`b` is linked to `c` with a `a` type link.

### usage: Implications
Any time a link is made, it's implied linkages are followed and generated.

### usage: Definitions
When processing a sentence, the definition of each word is looked up from the dictionary.

---------------

# Example

### General Rules:

	## General broad definitions
	the [noun] noun
	the [verb] verb
	
	## Specific Ideas
	is dog [noun]
	is cat [noun]
	
	## Processing
	the<1> # [noun]<2>

### Implications

#### is

	implies
		is [a] [b]
		->
			[b] [c] [d]
			[a] [c] [d]

--> Dec8.5

### Example sentence being processed

sentence: "The dog chases the cat"

	the [env_var_1] dog
	the [env_var_2] cat
	chases [env_var_1] [env_var_2]


### Example of boxing

The red dog chases the cat around the block. -->

                      +----------------+----+
	  +---------------+----+           |    |
	  +--+-------+    |    |           |    |
	  |  |   +---|    |    +--+---+    |    +--+----+
	  |  |   |   |    |    |  |   |    |    |  |    |
      # the red dog chases # the cat around # the block
	  +--+---+---+----+----+--+---+----+----+--+----+

Any word that is in a box, must link either to another word in the box, or one of the walls. 

The expected tree for the block structure above is:

	the [a] dog
	the [b] cat
	the [c] block
	is [a] red 
	is chases [d]
	[d] [a] [b]
	around [d] [c]