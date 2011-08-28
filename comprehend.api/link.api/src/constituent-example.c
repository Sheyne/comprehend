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

 /****************************************************************************
 *  
 *   This is a simple example of the link parser API to process constituents.
 *   The program prints out words at the leaves of the constituent tree,
 *   bracketing constituents labeled "PP" (prepositional phrase).
 ****************************************************************************/

void print_words_with_prep_phrases_marked(CNode *n) {
    CNode * m;
    static char * spacer=" ";

    if (n == NULL) return;
    if (strcmp(n->label, "PP")==0) {
	printf("%s[", spacer);
	spacer="";
    }
    for (m=n->child; m!=NULL; m=m->next) {
	if (m->child == NULL) {
	    printf("%s%s", spacer, m->label);
	    spacer=" ";
	}
	else {
	    print_words_with_prep_phrases_marked(m);
	}
    }
    if (strcmp(n->label, "PP")==0) {
	printf("]");
    }
}

int main() {

    Dictionary    dict;
    Parse_Options opts;
    Sentence      sent;
    Linkage       linkage;
    CNode *       cn;
    char *        string;
    char *        input_string = 
       "This is a test of the constituent code in the API.";

    opts  = parse_options_create();
    dict  = dictionary_create("4.0.dict", "4.0.knowledge", 
			      "4.0.constituent-knowledge", "4.0.affix");

    sent = sentence_create(input_string, dict);
    if (sentence_parse(sent, opts)) {
	linkage = linkage_create(0, sent, opts);
	printf("%s", string = linkage_print_diagram(linkage));
	string_delete(string);
	cn = linkage_constituent_tree(linkage);
	print_words_with_prep_phrases_marked(cn);
	linkage_free_constituent_tree(cn);
	fprintf(stdout, "\n\n");
	linkage_delete(linkage);
    }
    sentence_delete(sent);

    dictionary_delete(dict);
    parse_options_delete(opts);
    return 0;
}
