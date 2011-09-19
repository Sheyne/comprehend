//
//  ref_count.h
//  Comprehend
//
//  Created by Sheyne Anderson on 9/18/11.
//  Copyright 2011 Sheyne Anderson. All rights reserved.
//

#ifndef Comprehend_ref_count_h
#define Comprehend_ref_count_h

namespace ref_count {
	class Object{
		int ref_count;
	public:
		Object();
		Object *retain();
		Object *release();
	};
	
	
	class String: public Object{
	public:
		char data[];
		String(const char *string);
		~String();
	};
}
#endif
