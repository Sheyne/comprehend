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
 *   This is a version of the parser for use on the WWW.  
 *   Special properties:
 *      - no prompt
 *      - limit space and memory
 *      - limit link length
 *      - allows !mark to break up output
 *      - displays all or one linkage 
 *        (to demonstrate API)
 *     
 ****************************************************************************/

#include "link-includes.h"

#define MAXINPUT 1024
#define DISPLAY_MAX 100
#define COMMENT_CHAR '%'  /* input lines beginning with this are ignored */

#define DICTIONARY "/usr1/www/link/scripts/data/4.0.dict"  
   /* the path of the dictionary is used to lookup the following files and the word files */
#define AFFIX_FILE "4.0.affix"
#define PP_KNOWLEDGE "4.0.knowledge"
#define CONS_KNOWLEDGE "4.0.constituent-knowledge"

static int display_all;
static int max_sentence_length;
/* static int strip_preps; *DS*  */
static int min_short_sent_len=20;
static int use_postscript = 0;   /* this is obsolete, but I'll leave it here */

int fget_input_string(char *input_string, FILE *in, FILE *out, 
		      Parse_Options opts) {
    if (fgets(input_string, MAXINPUT, in)) return 1;
    else return 0;
}

char * obsolete_excise_prepositions(Linkage linkage, PostProcessor pp) {
    /* this function is obsolete *DS* */
    int w, l, r, link, num_words,j;
    int word_used[256];
    int word_is_in_prep_phrase[256];
    int in_prep_phrase, first_in_p, last_in_p;
    static char s[MAXINPUT];
    char t[MAXINPUT];
    Sentence sent;

    sent = linkage_get_sentence(linkage);
    linkage_post_process(linkage, pp);
    num_words = linkage_get_num_words(linkage);

    for (w=0; w<num_words; ++w) {
	word_used[w] = 0;
	word_is_in_prep_phrase[w] = 0;
    }

    linkage_compute_union(linkage);
    linkage_set_current_sublinkage(linkage, 
				   linkage_get_num_sublinkages(linkage)-1);

    for (w=0; w<num_words; ++w) {
	word_used[w] = 0;
    }

    /* First mark all words used in the linkage.  This will skip the conjunctions
       and words connected by null links, if any. */
    for (link=0; link<linkage_get_num_links(linkage); ++link) {
	l = linkage_get_link_lword(linkage, link);
	r = linkage_get_link_rword(linkage, link);
	if (l > 0) word_used[l] = 1;
	if (r < num_words-1) word_used[r] = 1;
    }

    /* Now mark all of the words that are used in a prepositional phrase */
    for (link=0; link<linkage_get_num_links(linkage); ++link) {
	if (linkage_get_link_num_domains(linkage, link) == 0) continue;
	l = linkage_get_link_lword(linkage, link);
	r = linkage_get_link_rword(linkage, link);
	if (l > 0) word_used[l] = 2;
	if (r < num_words) word_used[r] = 2;
    }

    /* Now, since prepositional phrases must consist of "contiguous" words,
       all unused words that appear in a string of contiguous 
       prepositional phrase words are labeled as belonging to the 
       prepositional phrase. This is how we handle 
       conjunctions (and null links) in prepositional phrases. */
    for (w=0; w<num_words; ++w) {
	if (word_used[w] == 2) {
	    first_in_p = last_in_p = w;
	    while (((word_used[w] == 2) || (word_used[w] == 0)) 
		   && (w < num_words)) {
		if (word_used[w] == 2) last_in_p = w;
		w++;
	    }
	    for (j=first_in_p; j<=last_in_p; ++j) {
		word_is_in_prep_phrase[j] = 1;
	    }
	}
    }

    /* Finally, print out the sentence, with the words appearing 
       in a prepositional phrase labeled "[...]" */
    in_prep_phrase = 0;
    s[0] = '\0';
    for (w=1; w<num_words-1; ++w) {
	if (word_is_in_prep_phrase[w]) {
	    if (!in_prep_phrase) {
		sprintf(t, "%s[", (w==1)?"":" ");
		strcat(s,t);
		in_prep_phrase = 1;
	    }
	    else {
		strcat(s, " ");
	    }
	    sprintf(t, "%s", sentence_get_word(sent, w));
	    strcat(s,t);
	}
	else {
	    if (in_prep_phrase) {
		strcat(s, "]");
		in_prep_phrase = 0;
	    }
	    sprintf(t, "%s%s", (w==1)?"":" ", sentence_get_word(sent, w));
	    strcat(s,t);
	}
    }
    if (in_prep_phrase) strcat(s, "]\n");
    else strcat(s,"\n");
    return s;
}


void process_linkage(Linkage linkage, Parse_Options opts) {
    char * string;
    int    j, mode;

    for (j=0; j<linkage_get_num_sublinkages(linkage); ++j) {
	linkage_set_current_sublinkage(linkage, j);
	if (parse_options_get_display_on(opts)) {
	    if (use_postscript) {
		string = linkage_print_postscript(linkage, 0);
	    } else {
		string = linkage_print_diagram(linkage);
	    }
	    fprintf(stdout, "%s", string);
	    string_delete(string);
	}
    }
    if ((mode=parse_options_get_display_constituents(opts))) {
	if (mode == 1) {
	    fprintf(stdout, "Constituent tree:\n\n");
	} else if (mode == 2) {
	    fprintf(stdout, "Constituent tree in bracked form:\n\n");
	}
	string = linkage_print_constituent_tree(linkage, mode);
	fprintf(stdout, "%s\n", string);
	string_delete(string);
    }
}

void print_parse_statistics(Sentence sent, Parse_Options opts) {
    if (sentence_num_linkages_found(sent) > 0) {
	fprintf(stdout, "Found %d linkage%s (%d with no P.P. violations)", 
		sentence_num_linkages_found(sent), 
		sentence_num_linkages_found(sent) == 1 ? "" : "s",
		sentence_num_valid_linkages(sent));
	if (sentence_null_count(sent) > 0) {
	    fprintf(stdout, " at null count %d", sentence_null_count(sent));
	}
	fprintf(stdout, "\n");
    }
}

void process_some_linkages(Sentence sent, Parse_Options opts) {
    int i, num_displayed, num_to_show;
    Linkage linkage;
    String_set * ss=NULL;
    /*     char * stripped_sent; *DS* */
   
    num_to_show = 
        MIN(sentence_num_valid_linkages(sent), display_all ? DISPLAY_MAX : 1);

    /* *DS 
    if (strip_preps) {
	ss = string_set_create();
    }
    else {
	print_parse_statistics(sent, opts);
    } */

    print_parse_statistics(sent, opts);
    for (i=0, num_displayed=0; i<num_to_show; ++i) {

	if (sentence_num_violations(sent, i) > 0)  continue;

	linkage = linkage_create(i, sent, opts);

	if (parse_options_get_display_on(opts)) {
	    if ((sentence_num_valid_linkages(sent) == 1) &&
		(!parse_options_get_display_bad(opts))) {
		fprintf(stdout, "  Unique linkage.");
	    }
	    else {
		fprintf(stdout, "  Linkage %d,", i+1);
	    }

	    fprintf(stdout, " cost vector = (UNUSED=%d DIS=%d AND=%d LEN=%d)\n",
		    linkage_unused_word_cost(linkage),
		    linkage_disjunct_cost(linkage),
		    linkage_and_cost(linkage),
		    linkage_link_cost(linkage));
	}

	/* *DS*
	if (strip_preps) {
	    stripped_sent = excise_prepositions(linkage, pp);
	    if (string_set_lookup(stripped_sent, ss) == NULL) {
		fprintf(stdout, stripped_sent);
		string_set_add(stripped_sent, ss);
	    }
	}
	else {
	    process_linkage(linkage, opts);
	}
	*/

	process_linkage(linkage, opts);

	linkage_delete(linkage);

    }

    /* *DS*    if (strip_preps) {
	string_set_delete(ss);
    }
    */

}

void clear_special_variables(Parse_Options opts) {
    display_all = 0;
    use_postscript = 0;
    parse_options_set_display_on(opts, 1);
    parse_options_set_display_constituents(opts, 0);
    parse_options_set_allow_null(opts, 1);
}

int special_command(char *input_string, Parse_Options opts, Dictionary dict) {

    if (input_string[0] == '\n') return TRUE;
    if (input_string[0] == COMMENT_CHAR) return TRUE;
    if (input_string[0] == '!') {
	input_string[strlen(input_string)-1] = '\0';
	if (strncmp("!mark", input_string, 5) == 0) {
	    fprintf(stdout, "mark: %s\n", input_string+6);
	    fflush(stdout);
	}
	else if (strncmp("!null=", input_string,6)==0) {
	    parse_options_set_allow_null(opts, atoi(input_string+6));
	}
	else if (strncmp("!justone=", input_string,9)==0) {
	    display_all = atoi(input_string+9) > 0 ? FALSE : TRUE;
	}
	else if (strncmp("!use-postscript=", input_string,16)==0) {
	    use_postscript = (atoi(input_string+16) != 0);
	}
	else if (strncmp("!constituents=", input_string,14)==0) {
 	    parse_options_set_display_constituents(opts, atoi(input_string+14));
	}
	else if (strncmp("!link-display=", input_string,14)==0) {
	    parse_options_set_display_on(opts, atoi(input_string+14));
	}
	/* *DS* 
	else if (strncmp("!strip-preps=", input_string,13)==0) {
	    strip_preps = atoi(input_string+13) > 0 ? TRUE : FALSE;
	    parse_options_set_display_on(opts, !strip_preps);
        }
	*/
	return TRUE;
    }
    return FALSE;
}

void setup_www_features(Parse_Options opts) {
    max_sentence_length = 70;
    parse_options_set_max_parse_time(opts, 10);
    parse_options_set_max_memory(opts, 128000000);
}

void setup_panic_parse_options(Parse_Options opts) {
    parse_options_set_disjunct_cost(opts, 3);
    parse_options_set_min_null_count(opts, 1);
    parse_options_set_max_null_count(opts, MAX_SENTENCE);
    parse_options_set_max_parse_time(opts, 60);
    parse_options_set_islands_ok(opts, 1);
    parse_options_set_short_length(opts, 6);
    parse_options_set_all_short_connectors(opts, 1);
    parse_options_set_linkage_limit(opts, 100);
}

int main(int argc, char * argv[]) {

    Dictionary      dict;
    Parse_Options   opts, panic_parse_opts;
    Sentence        sent;
    int             num_linkages;
    char            input_string[MAXINPUT];
    int             reported_leak, dictionary_and_option_space;

    if (argc != 1) {
        fprintf(stderr, "Usage: %s\n", argv[0]);
	exit(-1);
    }

    opts = parse_options_create();
    if (opts == NULL) {
	fprintf(stderr, "%s\n", lperrmsg);
	exit(-1);
    }
    panic_parse_opts = parse_options_create();
    if (panic_parse_opts == NULL) {
	fprintf(stderr, "%s\n", lperrmsg);
	exit(-1);
    }
    setup_panic_parse_options(panic_parse_opts);
    parse_options_set_panic_mode(opts, TRUE);

    dict = dictionary_create(DICTIONARY, PP_KNOWLEDGE, CONS_KNOWLEDGE, AFFIX_FILE);
    if (dict == NULL) {
	fprintf(stderr, "%s\n", lperrmsg);
	exit(-1);
    }

    /*    pp = post_process_open(NULL, PREP_KNOWLEDGE);   *DS*  */

    dictionary_and_option_space = space_in_use;  
    reported_leak = external_space_in_use = 0;

    setup_www_features(opts);

   /* clear_special_variables(opts); The www page should set all
          the vars to what it wants each time */

    while (fget_input_string(input_string, stdin, stdout, opts)) {
	if (space_in_use != dictionary_and_option_space + reported_leak) {
	    fprintf(stderr, "Warning: %d bytes of space leaked.\n",
		    space_in_use-dictionary_and_option_space-reported_leak);
	    reported_leak = space_in_use - dictionary_and_option_space;
	}

	if (special_command(input_string, opts, dict)) continue;

	sent = sentence_create(input_string, dict);
	if (sentence_length(sent) > max_sentence_length) {
	    sentence_delete(sent);
	    fprintf(stdout, "Sentence length (%d words) exceeds " \
		    "maximum allowable (%d words)\n",
		    sentence_length(sent), max_sentence_length);
	    continue;
	}
	if (sentence_length(sent) > min_short_sent_len) {
	    parse_options_set_short_length(opts, 6);
	}
	else {
	    parse_options_set_short_length(opts, max_sentence_length);
	}


	/* First parse with cost 0, 1 or 2 and no null links */
	parse_options_set_disjunct_cost(opts, 2);
	parse_options_set_min_null_count(opts, 0);
	parse_options_set_max_null_count(opts, 0);
	parse_options_reset_resources(opts);
	parse_options_set_linkage_limit(opts, 100);

	num_linkages = sentence_parse(sent, opts);

	/* Now parse with null links */
	if ((num_linkages == 0)) {
	    fprintf(stdout, "No complete linkages found.\n");
	    if (parse_options_get_allow_null(opts)) {
		parse_options_set_min_null_count(opts, 1);
		parse_options_set_max_null_count(opts, sentence_length(sent));
		num_linkages = sentence_parse(sent, opts);
	    }
	}

	if (parse_options_timer_expired(opts)) {
	    fprintf(stdout, "Timer is expired!\n");
	}
	if (parse_options_memory_exhausted(opts)) {
	    fprintf(stdout, "Memory is exhausted!\n");
	}

	if ((num_linkages == 0) && 
	    parse_options_resources_exhausted(opts) &&
	    parse_options_get_panic_mode(opts)) {
	    fprintf(stdout, "Entering \"panic\" mode...\n");
	    parse_options_reset_resources(panic_parse_opts);
	    num_linkages = sentence_parse(sent, panic_parse_opts);
	}

	print_total_time(opts);
	process_some_linkages(sent, opts);

	sentence_delete(sent);
	if (external_space_in_use != 0) {
	    fprintf(stderr, "Warning: %d bytes of external space leaked.\n", 
		    external_space_in_use);
	}
    }

    parse_options_delete(opts);
    /*    post_process_close(pp);  *DS* */
    dictionary_delete(dict);

    return 0;
}
