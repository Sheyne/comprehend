import linkgrammar
import comprehend

dict=linkgrammar.Dictionary("en")
sent = dict.Sentence("The dog has brown fur.")

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
			subject=comprehend.Phrase((link.right, link.left,), link.right)
	print subject, verb
	break