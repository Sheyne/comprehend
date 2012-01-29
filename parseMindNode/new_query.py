#! /usr/bin/env python

import shutil
import subprocess
import sys

queryname = 'queries/%s.mindnode' % sys.argv[1]

shutil.copy('resources/empty.mindnode', queryname)

subprocess.call(('open', queryname))