There are some relationships that the current system cannot convey. For example, that fact that any instance of 'dog' is also an instance if 'animal'. We cannot link 'dog --> animal', because the word dog is not an instance of animal. To represent this, the graphic system allows for the existence of some links to imply the presence of others. 

A rule in this form is called an implication and consists of two parts, a condition and implication. "Meeting a condition implies the implication." 


A sample dictionary containing an implication

	dog noun
	animal noun
	+?
		'?query -> dog'
	+implies
		"[query] -> animal"
		
		
--> How to implement such that implied links can imply other links? 
	Will I have to keep running the implication parser until no changes are made? 