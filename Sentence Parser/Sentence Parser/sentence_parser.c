//
//  sentence_parser.c
//  Sentence Parser
//
//  Created by Sheyne Anderson on 8/16/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "sentence_parser.h"

#define SPRetain(obj) obj;++obj->ref_count
#define SPRelease(obj) assert(obj->ref_count>0);\
	if (!--obj->ref_count) {\
		obj->dealloc(obj);\
		free(obj);\
		obj=NULL;\
	}

SPClassImplement(sp_type, sp_string type,{
	self->type=SPRetain(type);
},{
	SPRelease(self->type);
})
SPClassImplement(sp_string, char *value,{
	self->value=malloc(strlen(value));
	strcpy(self->value, value);
},{
	free(self->value);
})
void function(void);

void function(void){
	sp_string str=sp_string_alloc();
	str->init(str,"noun");
	sp_type type=sp_type_alloc();
	type->init(type,str);
}