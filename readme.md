Design criteria can be found [here](https://github.com/Sheyne/comprehend/wiki "On the wiki").
###The basics:

		+----------------Xp----------------+
		+-----Wd----+      +-----Os----+   |
		|      +-Ds-+--Ss--+     +--Ds-+   |
		|      |    |      |     |     |   |
	LEFT-WALL the boy.n threw.v the ball.n . 

should loosely translate to:

	struct environment *env = current_environment();
	
	struct svo *subject_verb_object = {
									   env->noun("the boy"),
									   env->verb("threw"),
									   env->noun("the ball")
									  };









Given the sentence, in past tense:

	The boy threw the ball.

and in the past progressive:
	
	The ball was thrown by the boy.
	
We see there are two sentences are equivalent, except that the subject and object switch places.

The system will automatically convert sentences to match the former. This makes an SVO set with "the boy" as the subject, "threw" as the verb, and "the ball" as the object.

Given the sentence:

	The ball was thrown.

This reformatting would result in a sentence with no subject. This is acceptable.