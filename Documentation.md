###Notes
for the purposes of this article, the documentation will mostly look like python.

Three underscores ( `___` ) in some code block denotes that this bit of code is irrelevant.

##Functions

####noun(env, name)
>Where env is the environment where the noun is being looked up, and name is a
string in the form of _"the cat"_, or _"Joe"_.

>If the noun is _"The cat"_, the environment will look for cats in reverse order and
return an array.

>So for example these sentences had been parsed:

>>The cat is asleep.

>>Another cat lies awake.

>And another sentence sentence contained _"the cat"_, when `noun("the cat")` was
called, the return value would be a reference to the second cat, then the first
cat.

>The same is true for statements like _"it"_ where it could be any number of things.
>>A posible addition would be to check if a value for it makes sense.

>>The same would definitely be done for words like he or she.

>`noun(__)` also performs **adjective parsing**: all of the `A` links to a noun
are added to a noun's adjective array.

####verb(name, subject, object=None)
>A verb is stored in with it's infinitive (the form that works after _"to"_ ex. 
_"to run"_) and tense. For example, _"ran"_ is stored as _"run"_ with tense
`past`. 

>In the sentence _"The boy threw"_,
Boy is the subject, and threw is the verb, so `verb("threw", noun(___,"the boy"))`
is called.
The return value of this is a verb with name: _"Throw"_, tense: `past`, and
subject is an instance of _"boy"_.




>In the sentence _"The boy threw the ball"_,

	           verb("threw",
	                 noun(___,"the boy"),
	                 noun(___,"the ball")
	           )
>is called.