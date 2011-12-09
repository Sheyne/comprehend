# Dictionary Rules

`a b c`: `a` is `b` linked to `c`

`[variable]`: a variable--can be used anywhere that a word could

`#`: generate a point that can be linked to with no name

`?`: query a word, and use it as the subject of the link

`[a]?`: same as `?`, but word must match `[a]`

`?[a]`: take a query and place it in variable `[a]`

### to define a  variable to a query:
`[x]` is `[]?`

### usage: Implications
any time a link is made, it's implications are followed and generated

### usage: Definitions
When processing a sentence, the definition of each word is looked up from the dictionary.

---------------

# Example

The dog chases the cat

### General Rules:

	[noun] the noun
	[verb] the verb
	dog is [noun]
	cat is [noun]

### Implications

#### is
given `a is b`

`b ?[c] ?[d]` -> 
`a [c] [d]`

### Definitions

#### the:
`# the [noun]?`

#### The beginning of an environment:

	[env_var_1] the dog
	[env_var_2] the cat
	[env_var_1] chases [env_var_2]



