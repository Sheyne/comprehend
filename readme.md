Design criteria can be found [here](https://github.com/Sheyne/comprehend/wiki "On the wiki").

##The basics:
Given the sentence, in past tense:

	The boy threw the ball.

and in the past progressive:
	
	The ball was thrown by the boy.
	
We see there are two sentences are equivalent, except that the subject and object switch.

The system will automatically convert sentences to match the former. This makes an SVO set with "the boy" as the subject, "threw" as the verb, and "the ball" as the object.

Given the sentence:

	The ball was thrown.

This reformatting would result in a sentence with no subject. This is acceptable.

A sentence also has a tense associated with it. 

	The boy threw the ball.
	
implies that

`The boy throws the ball.` or `The boy is throwing the ball.`
	
was true sometime in the past. The only difference is tense.

All these sentences should become something like:

	Enviroment env=Enviroment.current_enviroment()
	Sentence s=Sentence(enviroment=env)
	s.subject=env.noun("the boy")
	s.verb=env.verb("threw")  #internally becomes the infinitive.
	s.subject=env.noun("the ball")
	s.when=time.range(-∞, time.now(), inclusive=False)
	s.original_tense=null /*here I still need to come up with how to display this.*/


##Example cases:
###Present:
	Simple:			The boy throws the ball.
	Progressive:	The ball is thrown by the boy.

###Past:	
	Simple:			The boy threw the ball.
	Progressive:	The ball was thrown by the boy.

###Future:	
	Simple:			The boy will throw the ball.
	Progressive:	The ball will be thrown by the boy.

Article for easy refresh on verb tenses (here)[http://leo.stcloudstate.edu/grammar/tenses.html].
A pattern forms, progressive, the subject and object flip. The verb is more complicated, `throw`, present tense, is simple, and what everything should be refined down too. Present Progressing (`thrown`) is prefixed by an `is` and is constant between the the other tenses that are progressive. This allows us to determine tense based solely on the prefix. (`is`, `was`, `will be`).