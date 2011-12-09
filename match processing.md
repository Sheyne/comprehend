# Match processing
Look for a specific link structure.

reminder from the "Language Syntax Definition":

`[a]?[b]` means that find a structure that matches `[a]` and store it in `[b]`

given the structure

	[a] the dog
	[b] the cat
	[a] chases [b]

we can answer the question "What chases the cat", by matching the following:

	?[a] the cat
	?[match] chases [a]


## Topic of interest: Dec 8.1:
Should we eliminate queries? I think yes.

## Topic of interest: Dec 8.2:
How do we deal with the ambiguities that writing to a arrayed variable would cause?