emmit and request

any given word emmits a value, some can request other words before/after it

query: 
	
	"the"
	
do:	
	
	set: [a] ""
	require after: "[b]? type noun"
	make link: "[a] [b]"
	emmit: [a]
	
query:
	
	"type_verb verb"
	"[query]? type_verb verb"
	
do:
	
	require before: "[]"