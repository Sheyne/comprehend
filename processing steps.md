# Processing Steps

## 1. Tokenize sentence:
basically split the string into an array by SPACE chars. 

convert the word strings into their ID constants. (each usage of a word will have its own ID constant, and variations of the sentence with each usage will be formed.) 

send the variation as soon as it has been computed

one call to Tokenization, can result to multiple preprocessing calls

## 2. Preprocessing:
For every ID in the sentence, query DB for all instances of it's usage. (all links from/to the ID)

# Example Library (Under construction)
This is a basic 

### Basic grammars:
	[verb]--type--> verb
	[noun]--type--> noun
	[noun instance]--the--> [noun]	

### Definitions
	chases --same--> [verb]
	dog --same--> [noun]
	cat --same--> [noun]
	

### Enviroment
	Sam --is--> [noun instance](dog) ## discuss the verbage for this link...
	Sam --chases--> + --the--> cat