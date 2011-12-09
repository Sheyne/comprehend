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


##Top of question: Dec 8.1:
Should we eliminate queries? I think yes.