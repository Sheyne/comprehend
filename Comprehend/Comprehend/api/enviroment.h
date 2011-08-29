//
//  enviroment.h
//  Comprehend
//
//  Created by Sheyne Anderson on 8/28/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Comprehend_enviroment_h
#define Comprehend_enviroment_h

#include <stdbool.h>
#include <link-includes.h>

struct enviroment;

struct enviroment *enviroment_create(Dictionary dictionary, Parse_Options options);
void enviroment_set_tag(struct enviroment *enviroment, void *tag);
void enviroment_set_dictionary(struct enviroment *enviroment, Dictionary dictionary, bool managed);
void enviroment_set_parse_options(struct enviroment *enviroment, Parse_Options options, bool managed);
char *enviroment_get_tag(struct enviroment *enviroment);
Dictionary enviroment_get_dictionary(struct enviroment *enviroment);
Parse_Options enviroment_get_parse_options(struct enviroment *enviroment);
void enviroment_delete(struct enviroment *enviroment);

#endif
