import Tkinter as tk
import tkMessageBox
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
root.geometry("500x500")
panel1 = tk.Label(root, image=None)
panel1.pack(side='top', fill='both', expand='yes')
 
def sentence_caller(arg):
	try:
		g = parse_sentence(sentence.get().lower().replace(".", ""))
	except WordNotFound as w:
		tkMessageBox.showerror("Word Not Found", "I do not know the word \"%s\"" % str(w.args[0]))
	else:
		g.mutate(dictionary)
		database.add_info(g)
		buffer = withoutdictionary()
		print(buffer.edges)
		buffer = buffer.as_pydot_graph().create_png()
		buffer = StringIO(buffer)
		image1 = ImageTk.PhotoImage(Image.open(buffer))		 
		# get the image size
		w = image1.width()
		h = image1.height()
		sentence['width'] = w
		root.geometry("%dx%d" % (w, h+50))
		panel1['image'] = image1
		panel1.image = image1
		sentence.delete(0, tk.END)
	

sentence = tk.Entry(root, width = 500)
sentence.pack()
sentence.bind('<Return>',sentence_caller)
root.mainloop()