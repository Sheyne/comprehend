Design criteria can be found [here](https://github.com/Sheyne/comprehend/wiki "On the wiki").

##The basics:
Given the sentence, in past tense:

	The boy threw the ball.

and in the past progressive:
	
	The ball was thrown by the boy.
	
We see there are two sentences are equivalent, except that the subject and object switch. (The the doer becomes the object, and the doee becomes the subject.


##Object Structure.
A sentence structure has several components:

`Sentence`: An object for storing a sentence. 
 
 - `doer` `Noun`:
 	- What preformed an action.
 - `doee` `Noun`:
 	- What had an action performed on it.
 - `verb` `Verb`:
 	- What the action was.
 - `prepositions` `Preposition` array:
 	- Any conditions, or additional information. 

`Word`: Base class for all words

 - `word` `String`:
 	 - A `String` of the `Word`, and its most basic form.
 - `original_string` `String`:
 	 - Exactly what the parser received. (Often exactly the same as `word`).
 - `linked_words` `Word` array:
 	 - Any links this word had.

`Noun` (`Word`): Class for storing nouns

 - `word` `String`:
 	- In the context of a `Noun`, `word` means just the noun. So if `original_string` is `the dog`, then `word` is `dog`.

`Verb` (`Word`): Class for verbs

 - `word` `String`:
 	 - In the context of a `Verb`, `word` means the verb in present tense, with no extraneous words.
 - `tense` `Tense`:
 	 - If the word had any tense associated with it, store it here.
 	 
`Tense`: 
	
 - `simple` [past, present, or future]
 - `progressive` `Boolean`
 - `perfect` `Boolean`

##Link Grammar

		+-------------------Xp------------------+
		+-----Wd----+            +----Js----+   |
		|      +-Ds-+--Ss--+-MVp-+    +--Ds-+   |
		|      |    |      |     |    |     |   |
	LEFT-WALL the dog.n runs.v after the ball.s . 

Steps to translate the above link grammar into objects:

 1. We start by finding the `S` link.
 2. The left is the subject: store it in a variable as a noun.
 3. The right is the verb, store it in a variable as the verb. 
 4. Make a sentence object and set the verb to it.
 5. If the verb's tense is progressive, set the subject to the `doee`, otherwise set it the the `doer`. 


##Gerunds
Gerunds can be  converted to standard format as such:

`The dog is running.`:
Becomes: `The dog runs.`

`The dog is running after the ball.`:
Becomes: `The dog runs after the ball.`
