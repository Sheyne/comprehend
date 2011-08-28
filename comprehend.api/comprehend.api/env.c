//
//  env.c
//  Comprehend_api
//
//  Created by Sheyne Anderson on 8/27/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include "env.h"

struct env * env_make(char *id){
	struct env *enviroment;
	if((enviroment=malloc(sizeof(struct env)))){
		enviroment->id=id;
	}
	return enviroment;
}
void env_free(struct env *enviroment){
	free(enviroment);
}
