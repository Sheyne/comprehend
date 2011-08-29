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
	Dictionary	  dict;
	Parse_Options opts;
    Sentence      sent;
    Linkage       linkage;
    char *        diagram;
    int           i, num_linkages;
    char *        input_string[] = {
		"Grammar is useless because there is nothing to say -- Gertrude Stein.",
		"Computers are useless; they can only give you answers -- Pablo Picasso."};
	
    setlocale(LC_ALL, "");
	dict=dictionary_create_lang("en");
	opts=parse_options_create();
	parse_options_set_verbosity(opts, 0);
	if(dict)
		for (i=0; i<2; ++i) 
			if((sent = sentence_create(input_string[i], dict))){
				sentence_split(sent, opts);
				num_linkages = sentence_parse(sent, opts);
				if (num_linkages > 0) {
					linkage = linkage_create(0, sent, opts);
					printf("%s\n", diagram = linkage_print_diagram(linkage));
					linkage_free_diagram(diagram);
					linkage_delete(linkage);
				}
				sentence_delete(sent);
			}
	dictionary_delete(dict);
	parse_options_delete(opts);
    return 0;
}

