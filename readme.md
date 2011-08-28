Design criteria can be found [here](https://github.com/Sheyne/comprehend/wiki "On the wiki").
#The basics:

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
