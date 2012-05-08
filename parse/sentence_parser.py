from binary_sentence_parse import parse_sentence, WordNotFound
import graph as graphmodule

import mindnode
from magicate import prettify

dictionary = mindnode.mindmap('resources/dictionary.mindnode')

database = graphmodule.Graph()
database.mutate(dictionary)

def withoutdictionary():
	return database.combine(dictionary, set.difference)
last_query = None

while True:
	command = raw_input(": ").lower()
	if "?" == command:
		query = graphmodule.Graph()
		while True:
			line = raw_input("? ")
			if line == "":
				break
			else:
				query.add(*line.split(" "))
		print database.query(query)		
	elif command.endswith('.png'):
		withoutdictionary().as_pydot_graph().write_png(command)
	elif 'pp' == command:
		print prettify(withoutdictionary())
	elif "exit" == command:
		break
	elif ">" == command:
		while True:
			line = raw_input("> ")
			if line == "":
				break
			words = line.split(" ")
			if last_query is not None:
				words = tuple(last_query[word] if word in last_query else word for word in words)
			database.add(*words)
	else:
		try:
			g = parse_sentence(command.replace(".", ""))
		except WordNotFound as w:
			print "I do not know the word \"%s\"" % w
		else:
			g.mutate(dictionary)
			database.add_info(g)		