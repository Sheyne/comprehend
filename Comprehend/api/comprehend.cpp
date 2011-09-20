//
//  comprehend.cpp
//  Comprehend
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include "comprehend.h"
#include <stdio.h>
#include <vector>
#include <string.h>

namespace comprehend {

	Link::Link(const char *type, Word *target){
		_target=target;
		strcpy(_type,type);
		
	}
	Link::~Link(){

	}


	Word::Word(const char *word){
		size_t len=strlen(word)+1;
		_word=new char[len];
		memcpy(_word, word,len);

	}
	Word::~Word(){
	}
	void Word::add_link(Link *link){
		_links.push_back(link);
	}
	const char *Word::base_word(){
		return _word;
	}
	const std::vector <Link*>Word::links(){
		return _links;
	}
	
	
	Sentence::Sentence(Linkage linkage){
		int linkage_number, link_number, word_num;
		
		for (word_num=0; word_num<linkage_get_num_words(linkage); ++word_num){
			_words.push_back(new Word(linkage_get_word(linkage, word_num)));
		}
		
		for (linkage_number=0; linkage_number<linkage_get_num_sublinkages(linkage); ++linkage_number) {
			linkage_set_current_sublinkage(linkage, linkage_number);		
			
			for(link_number=0; link_number<linkage_get_num_links(linkage); ++link_number){
				int llw = linkage_get_link_lword(linkage, link_number);
				int lrw = linkage_get_link_rword(linkage, link_number);
				
				const char *link_label = linkage_get_link_label(linkage, link_number);
				
				_words[lrw]->add_link(new Link(link_label, _words[llw]));
				_words[llw]->add_link(new Link(link_label, _words[lrw]));
			}
		}
	}
	void Sentence::print_words(){
		printf("All words in the sentence.\n");
		for(std::vector<Word *>::iterator it = _words.begin(); it !=_words.end(); ++it) {			
			printf("word: %s --\n", (*it)->base_word());
		}
	}
	Sentence::~Sentence(){
		for(std::vector<Word *>::iterator it = _words.begin(); it !=_words.end(); ++it) {			

		}
	}
}