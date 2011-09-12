//
//  comprehend.h
//  Comprehend
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Comprehend_comprehend_h
#define Comprehend_comprehend_h
#include <set>
#include <string.h>

class Word {
public:
	const char *const name;
	bool operator == (Word other){
		return strcmp(other.name, name)==0;
	}
	Word(const char *name);
};

class Noun: public Word {	
public:
	Noun(const char*name):Word(name){}
};
class Enviroment {
	static Enviroment *standard_enviroment_;
public:
	std::set <Noun>nouns;
	static Enviroment *standard_enviroment(){
		if (!standard_enviroment_) {
			standard_enviroment_=new Enviroment;
		}
		return standard_enviroment_;
	}
};


#endif
