//
//  sentence_parser.c
//  Sentence Parser
//
//  Created by Sheyne Anderson on 8/16/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include <stdlib.h>
#include <assert.h>
#include "sentence_parser.h"

void SPRetain(sp_base obj){
	obj->ref_count++;
}
void SPRelease(sp_base obj){
	assert(obj->ref_count>0);
	if (!--obj->ref_count) {
		free(obj);
	}
}
