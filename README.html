<html>
	<head>
		<script src="http://shjs.sourceforge.net/sh_main.min.js"></script>
		<script src="http://shjs.sourceforge.net/lang/sh_c.min.js"></script>
		<link rel="stylesheet" type="text/css" href="http://shjs.sourceforge.net/sh_style.min.css" />
		<style>
			pre{
				border:1px dashed grey;
				overflow:auto;
			}
			pre.main_text{
				border:none;
				font:inherit;
			}
		</style>
	</head>
	<body onload="sh_highlightDocument();">
<h2>The basics:</h2>
with this defined:

<pre class="sh_c">
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
</pre>
then:
<pre class="sh_c">
    +----------------Xp----------------+
    +-----Wd----+      +-----Os----+   |
    |      +-Ds-+--Ss--+     +--Ds-+   |
    |      |    |      |     |     |   |
LEFT-WALL the boy.n threw.v the ball.n . 
</pre>

should loosely translate to:

<pre class="sh_c">

struct environment *env = current_environment();

struct noun *subject = env->noun("the boy");
struct noun *object  = env->noun("the ball");
struct verb *action  = env->verb("threw", object);

subject->do(action);
</pre>
which allows us to:
<pre class="sh_c">
noun *ball=env->noun("the ball");
noun *doer = ball->being[0]->doer; /* lets assume the first action that is
                                      happening to the ball is: being thrown*/
if(doer==env->noun("the boy")){ /* should evaluate to true */
	printf("The ball is being thrown by the boy.");
}
</pre>

The `env->noun(str)` function is the key part here. It's looks for a noun in `env`, 
and creates an instance if it cannot find one. It returns this. If multiple nouns
match str, it returns a NULL terminated array of nouns.<br /><br />

`env->verb(type, object)` creates a new verb with type, and sets object to be the
verb's object.


<pre class="sh_c">
struct noun *object  = env->noun("the ball");
struct verb *action  = env->verb("threw", object);
</pre>
In the above example, `action->object` is "the ball". This corresponds to the 
english statement, `who "threw" "the ball"?`

</body>
</html>