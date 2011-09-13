Design criteria can be found [here](https://github.com/Sheyne/comprehend/wiki "On the wiki").
###The basics:
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
