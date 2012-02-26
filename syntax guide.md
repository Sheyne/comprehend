# The Syntax Guide

## Components:

* `someword` -> `"someword"`;

* `@` -> shorthand for an anonymous node. Anonymous nodes are a special case in that they do not equal each other. Internally this is handled by renaming `@` to `@x`, where x is some globally unique name. All anonymous nodes are linked to `%anonymous`. 

* `?` works in a similar way to the `@` operator. 

* `[variable]` -> `"[variable]"`; but with some special properties to be discussed. 
 
## Operators:
* `(` and `)` -> link operators. Link the two things containd within parens.

* `!` -> the escape operator. If an object in a link has an `!` before it, the link is evaluated as that object. The first object in a linkage defaults to being escaped if neither are. 
 

	For example: 
	
		(((@ dog) !(@ chases)) quickly)
	
	Takes an anonymous node that points to dog, and points it to an anonymous node that points to chases. It then takes the anonymous node that points to chases and points it to quickly. 
	
* `?` searches for an existing linkage that satisfies the criteria. 

# Processing






### build a base dict
Each definition will have an array of associated words. These definition-word associations can be built from the query structure dictionary. 

### loop through sentence. 
for each word lookup all aplicable definitions and assume each is correct, splitting into seperate processess. 

the dog is red

	the:
		pull forward  					//look forward for an emiter that matches the following qq1
			{type_1 noun, ![type]? type_1}	//export the result of 
		do
			{type_1 [type], !@_1 type_1}
		!@_1
		
	dog:
		!$word
	
	is:
		with
		
		
## qq1
How do we determine what emiters to look for. 