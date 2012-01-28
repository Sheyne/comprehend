import graph


"""
Assign basic structures
-----------------------

@ the dog
@ the cat
@ the block


discuss complex interaction
---------------------------

{? the dog} chases {? the cat}
{{? the dog} ?chases {? the cat}} around {? the block}
{{? the dog} ?chases {? the cat}} at "3 PM"

simpler version of same interaction
-----------------------------------

{{? the dog} > ?chases > {? the cat}} >
	around > {? the block}
	at > "3 PM"

"""

"""
Key
====
@ -> new anonymous point
# -> what follows is optional
? -> what follows should jump from box
"""
all_nodes = set()

parse_word_state = {"words": (None, None), "doing now": "nothing"}

def parse_word(word):
	global parse_word_state
	parse_word_state['words'] = parse_word_state['words'][1], graph.Node(word)
	all_nodes.add(parse_word_state['words'][1])
	if parse_word_state['words'][0] and parse_word_state['words'][1]:
		parse_word_state['words'][0].point_at(parse_word_state['words'][1])


def parse_string(s):
	global all_nodes
	for line in filter(None,s.splitlines()):
		parse_word_state["doing now"]=">"		
		for word in filter(None,line.split(" ")):
			parse_word(word)
		parse_word_state["words"]=(None, None)		
parse_string("""
@ > the > dog
@ > the > cat
@ > the > block
""")


"""
all states know what to do with a word....
pull a word and determine which state it should be in
"""

