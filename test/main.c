//
//  main.c
//  test
//
//  Created by Sheyne Anderson on 8/27/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include <stdio.h>
#include "env.h"

int main (int argc, const char * argv[])
{
	struct env *enviroment=env_make("Hello");
	printf("the id is: %s\n", enviroment->id);
	env_free(enviroment);
	return 0;
}

