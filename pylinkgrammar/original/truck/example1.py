from linkgrammar import lp,Sentence,Linkage
parser = lp()

print "Using", parser.version

s = "Grammar is useless because there is nothing to say."
	
sent = Sentence(s)

print "Num linkages:",sent.parse()
	
linkage = Linkage(0,sent)
	
linkage.print_diagram()

# For now explicitly delete sentence
del linkage
del sent 


#clg.linkage_free_diagram(diagram)

