import os
import sys
from glob import glob

module = sys.argv[1]
for libpath in sys.path:
    for modpath in glob(os.path.join(libpath, module) + '*'):
        print modpath
        sys.exit(0)
print "Not Found."
