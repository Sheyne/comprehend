# Links

The basic link structure consists of: `{doer} -- {verb} -> {doee}`

Example: `[dog] -- is -> red`

The brackets around dog imply the bracketed object is an instance of `type`, or that # -- type -> dog, where the `#` represents the bracketed object. And is used in many cases when we are talking about an unnamed object. If we had said "Sam is a dog", It could translate to `Sam -- type -> dog`.

Not all of the objects need to be defined, with unknown objects being represented by a `#`.

Given the sentence, "The dog chases", we can translate that to: `[dog] -- chases -> #`. We are unsure of what the dog is chasing. 

Now suppose that we are given, "The dog chases the cat. ", we build the structure: `[dog] -- chases -> [cat]`. 

We can query the structure with questions. For example "What does the dog chase?". This becomes `[dog] -- chases -> ?`. This introduces the `?` token, which represents an unknown object that is being searched for. If the query was run on the above, `? = [cat]`.
