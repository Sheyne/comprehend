# Dictionary Rules

`a`: **word**--constant and global. (Technically a **global word**)

`[a]`: **scoped word**--can be used anywhere that a word could, but they have the benefit of scoping (`[b]` in one scope is not equal `[b]` in another scope).

`a<x>`: **word scan order**--scan the sentence for the word and plug in. The words need to be found in the sentence in the correct scan order. 

`#`: **anonymous word**--a each `#` is a unique word with no tag name.

`a b c`:linkage--`a` is linked to `c` with a `b` type link.

### usage: Implications
Any time a link is made, it's implied linkages are followed and generated.

### usage: Definitions
When processing a sentence, the definition of each word is looked up from the dictionary.

-------------------------------------------

# Example

### General Rules:

	## General broad definitions
	[noun] the noun
	[verb] the verb
	
	## Specific Ideas
	dog is [noun]
	cat is [noun]
	
	## Processing
	# the<1> [noun]<2>

### Implications

#### is

NEED TO RETHINK			
			

--> Dec8.5

### Example sentence being processed

sentence: "The dog chases the cat"

	[env_var_1] the dog
	[env_var_2] the cat
	[env_var_1] chases [env_var_2]


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

	[a] the dog
	[b] the cat
	[c] the block
	[a] is red 
	[d] is chases
	[a] [d] [b]
	[d] around [c]