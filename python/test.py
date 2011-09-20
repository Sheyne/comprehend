import linkgrammar
import comprehend
##############################################
## NEED TO ADD CODE TO STORE WORD POSITIONS ##
##############################################


for linkage in sent.linkages:
	print linkage
	subject = None
	object = None
	verb = None
	for link in linkage.links:
		if link.type.mayjor == "S":
			subject=link.left
			verb=link.right
	for link,direction in subject.links:
		if not direction and link.type.mayjor=="D":
			subject=comprehend.Phrase((link.left, link.right), link.right)
	print subject, verb
	break