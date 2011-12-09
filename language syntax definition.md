# Dictionary Rules

`a`: **word**--constant and global. (Technically a **global word**)

`[a]`: **scoped word**--can be used anywhere that a word could, but they have the benefit of scoping (`[b]` in one scope is not equal `[b]` in another scope).

`<a>`: **scan word**--scan the sentence for the word and plug in. Can be scoped or global. 

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
	<the> # <[noun]>

### Implications

#### is
given `a is b`

`b [c] [d]` -> 
`a [c] [d]`

### Example sentence being processed

sentence: "The dog chases the cat"

	the [env_var_1] dog
	the [env_var_2] cat
	chases [env_var_1] [env_var_2]


# Thoughts log
## Dec8.3:
**On infix notation**

this constitutes a switch to prefix notation for links

## Dec8.4:
**on scan words, and loading.**

scan order, left, right, and boxing

#### Links should have direction:
`Dog` should not use a `the` that comes after it in a sentence. At least in most cases

#### Links should form boxes:
all adjectives between a linked `the` and `dog` should be captured.











