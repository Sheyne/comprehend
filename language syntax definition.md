##Link grammar:

The dog chases the cat

#### General Rules:

	[noun] the noun
	[verb] the verb
	dog is [noun]
	cat is [noun]

### Implications

#### is
given `a is b`
for each `b ?[c] ?[d]` -> 
`a [c] [d]`

### Definitions

#### the:
`# the [noun]?`

#### The beginning of an environment:

	[var_num_1] the dog
	[var_num_1] chases [var_num_2]
	[var_num_2] the cat



# Dictionary Rules

`a b c`: `a` is `b` linked to `c`

`[variable]`: a variable--can be used anywhere that a word could

`#`: generate a point that can be linked to with no name

`?`: query a word, and use it as the subject of the link

`[a]?`: same as `?`, but word must match `[a]`

`?[a]`: take a query and place it in variable `[a]`

### to define a  variable to a query:

`[x]` is `[]?`
	