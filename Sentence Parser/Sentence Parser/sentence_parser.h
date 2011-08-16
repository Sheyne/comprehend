//
//  sentence_parser.h
//  Sentence Parser
//
//  Created by Sheyne Anderson on 8/16/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Sentence_Parser_sentence_parser_h
#define Sentence_Parser_sentence_parser_h


/*abstract base type for all classes to inherit from, all sp_classes inherit by prefixing
 their declairation with struct sp_base super.*/

#define SPClass(_name,_base, _content) struct _name{struct _base super;_content};\
typedef struct _name *_name

SPClass(sp_base,,
		int ref_count;
		);

SPClass(sp_type, sp_base,
		char*type;
		);
SPClass(sp_punctuation, sp_base,
		char punctuation;
		);
SPClass(sp_word, sp_base,
		char *word;
		sp_type *types;
		);

void SPRetain(sp_base obj);
void SPRelease(sp_base obj);

sp_type SPMakeType(char *type);
sp_word SPWordType(char *word, sp_type types[0]);
sp_punctuation SPMakePunctuation(char punctuation);

typedef sp_base sp_sentence[0];
/* An array of sp_words terminated by a sp_punctuation. */

sp_type SPTypeOfWord(sp_word word);


extern const sp_punctuation *sp_period, *sp_comma, sp_exclamation;


#endif
