//
//  comprehend.h
//  Comprehend
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Comprehend_comprehend_h
#define Comprehend_comprehend_h
#include <vector>

#include "ref_count.h"
using namespace ref_count;

class Word;

class Link: public Object {
	String *_type;
	Word *_target;
public:
	Link(String *type, Word *target);
	Link(const char *type, Word *target);
	~Link();
};

class Word: public Object {
	std::vector <Link*> links;
	String *_word;
public:
	void add_link(Link *link){
		links.push_back(link);
	}
	
	String * base_word(){
		return _word;
	}
	Word(String *word);
	Word(const char *word);
	~Word();
};

#endif
