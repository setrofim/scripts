#!/usr/bin/env python
"""
Ghetto man replacement for GnuWin32.

"""
import os
import sys
import string
from subprocess import call, Popen, PIPE
from optparse import OptionParser

__author__ = 'setrofim'
__version__ = '0.1'


tp = Popen('uname', stdout=PIPE, stderr=PIPE, shell=True)
out, err = tp.communicate()
if out.startswith('MINGW32'):
    os.sep = '/'


GNUWIN32 = os.getenv('GNUWIN32') or r'C:\Apps\GnuWin32'
DEFAULT_MAN_PAGES_PATH = os.path.join(GNUWIN32, 'man')
FIND = os.path.join(GNUWIN32, 'bin', 'find.exe')
MAN_PAGES_PATH = os.getenv('MAN_PAGES_PATH') or DEFAULT_MAN_PAGES_PATH
PAGER = os.getenv('PAGER') or os.path.join(GNUWIN32, 'bin', 'less_.exe')


def check_environment():
    for path in [GNUWIN32, DEFAULT_MAN_PAGES_PATH, FIND]:
        if not os.path.exists(path):
            raise Exception("Can't find {0}; is GNUWIN32 set correctly?".format(path))


def error(message):
    sys.stderr.write('ERROR: {0}\n'.format(message))
    parser.print_help()
    sys.exit(1)


def process_arguments(parser):
    opts, args = parser.parse_args()
    if len(args) == 2:
        category = args[0]
        if not(len(category) <= 2 and category[0] in string.digits):
            raise Exception('Invalid category: {0}'.format(category))
        item = args[1]
    elif len(args) == 1:
        category = '*'
        item =  args[0]
    else:
        raise Exception('Incorrect number of arguments.')
    return category, item, opts


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: man.py [options] [CATEGORY] PROGRAM')
    parser.add_option('-a', dest='all', action='store_true',
                      help='Display all matching entries (by default, only the first one).')
    parser.add_option('-i', dest='nocase', action='store_true',
                      help='Case insensitive search.')
    try:
        check_environment()
        category, item, opts = process_arguments(parser)
    except Exception, e:
        error(str(e))

    namepred = opts.nocase and 'iname' or 'name'

    command = '{0} {4}{5}cat{1} -{2} {3}.{1}.txt'.format(FIND,
                                                         category,
                                                         namepred,
                                                         item,
                                                         MAN_PAGES_PATH,
                                                         os.sep)
    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    if err:
        error(err)
    paths = [ p.rstrip('\r\n') for p in out.split('\n') if p.rstrip('\r\n')]

    if paths:
        if opts.all:
            args = [PAGER]
            args.extend(paths)
            call(args, shell=True)
        else:
            call([PAGER, paths[0]], shell=True)
    else:
        sys.stderr.write('Could not find {0}.\n'.format(item))
        sys.exit(2)


