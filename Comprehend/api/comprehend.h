//
//  comprehend.h
//  Comprehend
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Comprehend_comprehend_h
#define Comprehend_comprehend_h
#include <vector>
#include <link-includes.h>



namespace comprehend {
	class Word;

	class Link {
		Word *_target;
		char _type[];
	public:
		Link(const char *type, Word *target);
		~Link();
	};

	class Word {
		std::vector <Link*> _links;
		char *_word;
	public:
		void add_link(Link *link);
		const std::vector <Link*>links();
		const char * base_word();
		Word(const char *word);
		~Word();
	};

	class Sentence {
		std::vector<Word *> _words;
	public:
		Sentence(Linkage linkage);
		~Sentence();
		void print_words();
	};

}

#endif
