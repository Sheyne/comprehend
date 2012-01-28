When a client connects to a server, join a context. These contexts are persistent and unique. They can be thought of as environments where something happens. 


Each query is in it's own scope. Further scoping can be indicated with indentation.

Assuming the following is entered into a context:

	Sam the dog
	µ the cat
	Sam chases µ

And later the following is entered in the same context:

	Sam chases [a]

The server would respond with all possible values for `[a]` in this case only `µ`.
