//
//  ref_count.cpp
//  Comprehend
//
//  Created by Sheyne Anderson on 9/18/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include "ref_count.h"
#include <stdio.h>
#include <string.h>

using namespace ref_count;

Object * Object::retain(){
	++ref_count;
	return this;
}
Object * Object::release(){
	if(--ref_count<=0){
		delete this;
	}
	return NULL;
}
Object::Object(){
	ref_count=0;
	this->retain();
}

String::String(const char *string){
	Object::Object();
	strcpy(data, string);
}
String::~String(){
	
}