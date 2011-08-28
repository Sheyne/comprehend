Documentation can be found [here](https://github.com/Sheyne/comprehend/wiki "On the wiki").

#The basics:
with this defined:

	struct word{
		char *tag;
	};
	struct verb;
	struct noun{
		struct word;
		struct verb doing[0];
		struct vern being[0];
		struct adjective adjectives[0];
	};
	struct verb{
		struct word;
		struct noun *doer;
		struct noun *object;
		struct adverb adverbs[0];
	};
then:

		+----------------Xp----------------+
		+-----Wd----+      +-----Os----+   |
		|      +-Ds-+--Ss--+     +--Ds-+   |
		|      |    |      |     |     |   |
	LEFT-WALL the boy.n threw.v the ball.n . 

should loosely translate to:

	struct environment *env = current_environment();
	
	struct noun *subject = env->noun("the boy");
	struct noun *object  = env->noun("the ball");
	struct verb *action  = env->verb("threw", object);
	
	subject->do(action);

which allows us to:

	noun *ball=env->noun("the ball");
	noun *doer = ball->being[0]->doer; /* lets assume the first action that is
										  happening to the ball is: being thrown*/
	if(doer==env->noun("the boy")){ /* should evaluate to true */
		printf("The ball is being thrown by the boy.");
	}

The `env->noun(str)` function is the key part here. It's looks for a noun in `env`, 
and creates an instance if it cannot find one. It returns this. If multiple nouns
match str, it returns a NULL terminated array of nouns.<br /><br />

`env->verb(type, object)` creates a new verb with type, and sets object to be the
verb's object.

	struct noun *object  = env->noun("the ball");
	struct verb *action  = env->verb("threw", object);

In the above example, `action->object` is "the ball". This corresponds to the 
english statement, `who "threw" "the ball"?`