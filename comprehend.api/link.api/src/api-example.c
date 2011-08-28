/********************************************************************************/
/* Copyright (c) 2004                                                           */
/* Daniel Sleator, David Temperley, and John Lafferty                           */
/* All rights reserved                                                          */
/*                                                                              */
/* Use of the link grammar parsing system is subject to the terms of the        */
/* license set forth in the LICENSE file included with this software,           */ 
/* and also available at http://www.link.cs.cmu.edu/link/license.html           */
/* This license allows free redistribution and use in source and binary         */
/* forms, with or without modification, subject to certain conditions.          */
/*                                                                              */
/********************************************************************************/

#include "link-includes.h"

int main() {

    Dictionary    dict;
    Parse_Options opts;
    Sentence      sent;
    Linkage       linkage;
    char *        diagram;
    int           i, num_linkages;
    char *        input_string[] = {
       "Grammar is useless because there is nothing to say -- Gertrude Stein.",
       "Computers are useless; they can only give you answers -- Pablo Picasso."};

    opts  = parse_options_create();
    dict  = dictionary_create("4.0.dict", "4.0.knowledge", NULL, "4.0.affix");

    for (i=0; i<2; ++i) {
	sent = sentence_create(input_string[i], dict);
	num_linkages = sentence_parse(sent, opts);
	if (num_linkages > 0) {
	    linkage = linkage_create(0, sent, opts);
	    printf("%s\n", diagram = linkage_print_diagram(linkage));
	    string_delete(diagram);
	    linkage_delete(linkage);
	}
	sentence_delete(sent);
    }

    dictionary_delete(dict);
    parse_options_delete(opts);
    return 0;
}
