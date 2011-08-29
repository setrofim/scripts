#!/usr/bin/env python
"""
scandocument.py -- Scans a multi-page documents into a .pdf.

Copyright (c) 2011 Sergei Trofimov setrofim@gmail.com.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

__author__ = 'Sergei Trofimov'
__version__ = (0, 1, 0)

import os
import sys
import logging
from glob import glob
from tempfile import mkdtemp

logging.basicConfig(level=logging.DEBUG)

scanimage = '/usr/bin/scanimage'
scanimage_opts = {
        'resolution':300,
        'format':'tiff',
        }
tiff2ps = '/usr/bin/tiff2ps'
ps2pdf = '/usr/bin/ps2pdf'
pdfjoin = '/usr/bin/pdfjoin'

def make_command(cmd, args, opts):
    return ' '.join([cmd, 
                     ' '.join(['--{0}={1}'.format(*i) for i in opts.items()]),
                     ' '.join(map(str, args)),
                   ])

def get_response(message):
    resp = raw_input(message + ' yes/no: [yes]').lower()
    while True:
        if resp in 'yes':
            return True
        elif resp in 'no':
            return False
        else:
            resp = raw_input(message + ' yes/no: [yes]').lower()

def execute_command(commandstring):
    logging.debug('executing: {0}'.format(commandstring))
    res = os.system(commandstring)
    logging.debug('returned: {0}'.format(res))

def scan_page(cmd, cmdopts, outdir, pageno):
    outfile = os.path.join(outdir, ''.join([os.path.basename(cmd), str(pageno), '.tiff']))
    args = [' '.join(['>', outfile]),]
    commandstring = make_command(scanimage, args, scanimage_opts)
    execute_command(commandstring)
    return get_response('Scan the next page?')

def convert_to_pdf(workdir):
    for filepath in glob(os.path.join(workdir, '*.tiff')):
        print '.',
        basename = os.path.splitext(filepath)[0]
        psfile = basename + '.ps'
        commandstring = '{0} {1} > {2}'.format(tiff2ps, filepath, psfile)
        execute_command(commandstring)
        logging.debug('removing {0}'.format(filepath))
        os.remove(filepath)
        pdffile = basename + '.pdf'
        commandstring = '{0} {1} {2}'.format(ps2pdf, psfile, pdffile)
        execute_command(commandstring)
        logging.debug('removing {0}'.format(psfile))
        os.remove(psfile)
    print

def join_pdf_pages(workdir, outfile):
    tempfiles = os.path.join(workdir, '*.pdf')
    commandstring = '{0} {1} -o \'{2}\''.format(pdfjoin, ' '.join(glob(tempfiles)), outfile)
    execute_command(commandstring)
    logging.debug('removing ' + tempfiles)
    for f in glob(tempfiles):
        os.remove(f)

if __name__ == '__main__':
    workdir = mkdtemp()
    logging.debug('using temp dir: {0}'.format(workdir))
    raw_input('Insert the first page into the scanner and press return.')
    page_count = 1
    while scan_page(scanimage, scanimage_opts, workdir, page_count):
        page_count += 1
    print 'Converting...'
    convert_to_pdf(workdir)
    if len(sys.argv) > 1:
        outfile = sys.argv[1]
    else:
        outfile = raw_input('Please specify output file: ')
        if not outfile.lower().endswith('.pdf'):
            outfile += '.pdf'
    logging.debug('writing to ' + outfile)
    print 'Writing output.'
    join_pdf_pages(workdir, outfile)
    logging.debug('removing ' + workdir)
    os.rmdir(workdir)
    print 'Done.'

