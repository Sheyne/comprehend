//
//  comprehend.cpp
//  Comprehend
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include "comprehend.h"
#include <stdio.h>

Link::Link(const char *type, Word *target){
	_target=target;
	_target->retain();
	_type=new String(type);
}
Link::Link(String *type, Word *target){
	_target=target;
	_target->retain();
	_type=type;
	_type->retain();
}
Link::~Link(){
	_type->release();
	_type=NULL;
	_target->release();
	_target=NULL;
}



Word::Word(const char *word){
	_word=new String(word);
}

Word::Word(String *word){
	_word=word;
	_word->retain();
}
Word::~Word(){
	_word->release();
	_word=NULL;
}