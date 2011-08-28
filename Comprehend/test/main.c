//
//  main.c
//  test
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include <locale.h>
#include <stdio.h>
#include <stdbool.h>
#include <link-includes.h>
#include "enviroment.h"

int main (int argc, const char * argv[])
{
	struct enviroment *env;
    Sentence      sent;
    Linkage       linkage;
    char *        diagram;
    int           i, num_linkages;
    char *        input_string[] = {
		"Grammar is useless because there is nothing to say -- Gertrude Stein.",
		"Computers are useless; they can only give you answers -- Pablo Picasso."};
	
    setlocale(LC_ALL, "");
	env=enviroment_create(NULL, NULL);
	parse_options_set_verbosity(enviroment_get_parse_options(env), 0);
	if(enviroment_get_dictionary(env))
		for (i=0; i<2; ++i) 
			if((sent = sentence_create(input_string[i], enviroment_get_dictionary(env)))){
				sentence_split(sent, enviroment_get_parse_options(env));
				num_linkages = sentence_parse(sent, enviroment_get_parse_options(env));
				if (num_linkages > 0) {
					linkage = linkage_create(0, sent, enviroment_get_parse_options(env));
					printf("%s\n", diagram = linkage_print_diagram(linkage));
					linkage_free_diagram(diagram);
					linkage_delete(linkage);
				}
				sentence_delete(sent);
			}
	enviroment_delete(env);
    return 0;
}

