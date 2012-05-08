import Tkinter as tk
from PIL import Image, ImageTk
from StringIO import StringIO
from binary_sentence_parse import parse_sentence, WordNotFound
import graph as graphmodule
import mindnode
from magicate import shorten

dictionary = mindnode.mindmap('resources/dictionary.mindnode')

database = graphmodule.Graph()
database.mutate(dictionary)

def withoutdictionary():
	return shorten(database.combine(dictionary, set.difference))
root = tk.Tk()
root.title('Sentence Graph')
 
x = 0
y = 0
h = 500
w = 500
root.geometry("%dx%d+%d+%d" % (w, h+50, x, y))
panel1 = tk.Label(root, image=None)
panel1.pack(side='top', fill='both', expand='yes')
 
def sentence_caller(arg):
	try:
		g = parse_sentence(sentence.get().lower().replace(".", ""))
	except WordNotFound as w:
		print "I do not know the word \"%s\"" % w
	else:
		g.mutate(dictionary)
		database.add_info(g)
		buffer = withoutdictionary()
		print buffer.edges
		buffer = buffer.as_pydot_graph().create_png()
		buffer = StringIO(buffer)
		image1 = ImageTk.PhotoImage(Image.open(buffer))		 
		# get the image size
		w = image1.width()
		h = image1.height()
		root.geometry("%dx%d" % (w, h+50))
		panel1['image'] = image1
		panel1.image = image1
		sentence.delete(0, tk.END)
	

sentence = tk.Entry(root, width=w)
sentence.pack()
sentence.bind('<Return>',sentence_caller)
root.mainloop()