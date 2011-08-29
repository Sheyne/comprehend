//
//  enviroment.c
//  Comprehend
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#include <stdlib.h>
#include "enviroment.h"


struct  enviroment{
	void *tag;
    Dictionary dictionary;
    Parse_Options options;
	unsigned char mmconf;
};
enum enviroment_mmconfs {
	enviroment_mmconf_dictionary_is_managed = 0b00001,
	enviroment_mmconf_options_is_managed    = 0b00010
	};

struct enviroment *enviroment_create(Dictionary dictionary, Parse_Options options){
	struct enviroment *enviroment=malloc(sizeof(struct enviroment));
	enviroment->mmconf=0;
	if (enviroment) {
		if (dictionary) {
			enviroment->dictionary=dictionary;
		}else{
			enviroment->mmconf |= enviroment_mmconf_dictionary_is_managed;
			enviroment->dictionary = dictionary_create_lang("en");
		}
		if(options){
			enviroment->options=options;
		}else{
			enviroment->mmconf |= enviroment_mmconf_options_is_managed;
			enviroment->options = parse_options_create();
		}
	}
	return enviroment;
}
void enviroment_set_tag(struct enviroment *enviroment, void *tag){
	enviroment->tag=tag;
}
void enviroment_set_dictionary(struct enviroment *enviroment, Dictionary dictionary, bool managed){
	enviroment->dictionary=dictionary;
	if (managed)
		enviroment->mmconf |= enviroment_mmconf_dictionary_is_managed;
	else
		enviroment->mmconf &=~enviroment_mmconf_dictionary_is_managed;
}
void enviroment_set_parse_options(struct enviroment *enviroment, Parse_Options options, bool managed){
	enviroment->options=options;
	if (managed)
		enviroment->mmconf |= enviroment_mmconf_options_is_managed;
	else
		enviroment->mmconf &=~enviroment_mmconf_options_is_managed;
}
void enviroment_delete(struct enviroment *enviroment){
	if (enviroment->mmconf & enviroment_mmconf_dictionary_is_managed)
		dictionary_delete(enviroment->dictionary);
	if (enviroment->mmconf & enviroment_mmconf_options_is_managed)
		parse_options_delete(enviroment->options);
	free(enviroment);
}


char *enviroment_get_tag(struct enviroment *enviroment){ return enviroment->tag; }
Dictionary enviroment_get_dictionary(struct enviroment *enviroment){ return enviroment->dictionary; }
Parse_Options enviroment_get_parse_options(struct enviroment *enviroment){ return enviroment->options; }

