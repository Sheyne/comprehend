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
#include <math.h>
#include <vector>

std::vector<Word*> process_linkage_test(Linkage linkage);

std::vector<Word*> process_linkage_test(Linkage linkage){
	int linkage_number, link_number, word_num;
	
	std::vector<Word*> words(linkage_get_num_words(linkage));
	
	for (word_num=0; word_num<linkage_get_num_words(linkage); ++word_num){
		words[word_num]=new Word(linkage_get_word(linkage, word_num));
	}
	
	for (linkage_number=0; linkage_number<linkage_get_num_sublinkages(linkage); ++linkage_number) {
		linkage_set_current_sublinkage(linkage, linkage_number);		
		
		for(link_number=0; link_number<linkage_get_num_links(linkage); ++link_number){
			int llw = linkage_get_link_lword(linkage, link_number);
			int lrw = linkage_get_link_rword(linkage, link_number);

			const char *link_label = linkage_get_link_label(linkage, link_number);
						
			words[lrw]->add_link(new Link(link_label, words[llw]));
			words[llw]->add_link(new Link(link_label, words[lrw]));
		}
	}
	return words;
}
using namespace ref_count;

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
					process_linkage_test(linkage);
					linkage_free_diagram(diagram);
					linkage_delete(linkage);
				}
				sentence_delete(sent);
			}
	dictionary_delete(dict);
	parse_options_delete(opts);
    return 0;
}

