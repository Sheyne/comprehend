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
#include "comprehend.h"

int main (int argc, const char * argv[])
{		
	Dictionary	  dict;
	Parse_Options opts;
    Sentence      sent;
    Linkage       linkage;
    char *        diagram;
    int           i, num_linkages;
    const char *        input_string[] = {"the dog is black."};
	
    setlocale(LC_ALL, "");
	dict=dictionary_create_lang("en");
	opts=parse_options_create();
	parse_options_set_verbosity(opts, 0);
	if(dict)
		for (i=0; i<1; ++i) 
			if((sent = sentence_create(input_string[i], dict))){
				sentence_split(sent, opts);
				num_linkages = sentence_parse(sent, opts);
				if (num_linkages > 0) {
					linkage = linkage_create(0, sent, opts);
					printf("%s\n", diagram = linkage_print_diagram(linkage));
					comprehend::Sentence *sen=new comprehend::Sentence(linkage);
					sen->print_words();
					linkage_free_diagram(diagram);
					linkage_delete(linkage);
				}
				sentence_delete(sent);
			}
	dictionary_delete(dict);
	parse_options_delete(opts);
    return 0;
}

