//
//  env.h
//  Comprehend_api
//
//  Created by Sheyne Anderson on 8/27/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Comprehend_api_env_h
#define Comprehend_api_env_h

struct env {
	char *id;
	char *nouns;
};

struct env * env_make(char *id);
void env_free(struct env *enviroment);

#endif
