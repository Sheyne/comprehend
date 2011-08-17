//
//  sentence_parser.h
//  Sentence Parser
//
//  Created by Sheyne Anderson on 8/16/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Sentence_Parser_sentence_parser_h
#define Sentence_Parser_sentence_parser_h


#define SPClassImplement(name, args, init_, dealloc_) \
void name##_init(name self, args){init_}\
void name##_dealloc(name self){dealloc_}\
name name##_alloc(){\
name self=malloc(sizeof(struct name));\
self->dealloc=name##_dealloc;\
self->init=name##_init;\
return self;\
}

#define SPClass(_name,_base, args, _content) \
struct _name;\
typedef struct _name *_name;\
struct _name{struct _base super;int ref_count;void (*dealloc)(_name self);void (*init)(_name self, args);_content};\
void _name##_dealloc(_name self) ; \
void _name##_init(_name self, args); \
_name _name##_alloc(void);


SPClass(sp_base,{},void *unused,)
SPClass(sp_string, sp_base, char *value, char*value;)
SPClass(sp_type, sp_base,sp_string type,sp_string type;)
SPClass(sp_punctuation, sp_base,char punctuation,char punctuation;)
SPClass(sp_word, sp_base,char *word,char *word;sp_type *types;)

void SPRetain(sp_base obj);
void SPRelease(sp_base obj);


typedef sp_base sp_sentence[0];
/* An array of sp_words terminated by a sp_punctuation. */

sp_type SPTypeOfWord(sp_word word);


extern const sp_punctuation *sp_period, *sp_comma, sp_exclamation;


#endif
