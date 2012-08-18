#!/usr/bin/env python
"""Generate the errorcodes module starting from PostgreSQL documentation.

The script can be run at a new PostgreSQL release to refresh the module.
"""

# Copyright (C) 2010 Daniele Varrazzo  <daniele.varrazzo@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

import sys
import urllib2
from collections import defaultdict

from BeautifulSoup import BeautifulSoup as BS

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "usage: %s /path/to/errorcodes.py" % sys.argv[0]
        return 2

    filename = sys.argv[1]

    file_start = read_base_file(filename)
    classes, errors = fetch_errors(['8.1', '8.2', '8.3', '8.4', '9.0', '9.1'])

    f = open(filename, "w")
    for line in file_start:
        print >>f, line
    for line in generate_module_data(classes, errors):
        print >>f, line

def read_base_file(filename):
    rv = []
    for line in open(filename):
        rv.append(line.rstrip("\n"))
        if line.startswith("# autogenerated"):
            return rv

    raise ValueError("can't find the separator. Is this the right file?")

def parse_errors(url):
    page = BS(urllib2.urlopen(url))
    table = page('table')[1]('tbody')[0]

    classes = {}
    errors = defaultdict(dict)

    for tr in table('tr'):
        if tr.td.get('colspan'): # it's a class
            label = ' '.join(' '.join(tr(text=True)).split()) \
                .replace(u'\u2014', '-').encode('ascii')
            assert label.startswith('Class')
            class_ = label.split()[1]
            assert len(class_) == 2
            classes[class_] = label

        else: # it's an error
            errcode = tr.tt.string.encode("ascii")
            assert len(errcode) == 5

            tds = tr('td')
            if len(tds) == 3:
                errlabel = '_'.join(tds[1].string.split()).encode('ascii')

                # double check the columns are equal
                cond_name = tds[2].string.strip().upper().encode("ascii")
                assert errlabel == cond_name, tr

            elif len(tds) == 2:
                # found in PG 9.1 docs
                errlabel = tds[1].tt.string.upper().encode("ascii")

            else:
                assert False, tr

            errors[class_][errcode] = errlabel

    return classes, errors

errors_url="http://www.postgresql.org/docs/%s/static/errcodes-appendix.html"

def fetch_errors(versions):
    classes = {}
    errors = defaultdict(dict)

    for version in versions:
        c1, e1 = parse_errors(errors_url % version)
        classes.update(c1)
        for c, cerrs in e1.iteritems():
            errors[c].update(cerrs)

    return classes, errors

def generate_module_data(classes, errors):
    yield ""
    yield "# Error classes"
    for clscode, clslabel in sorted(classes.items()):
        err = clslabel.split(" - ")[1].split("(")[0] \
                .strip().replace(" ", "_").replace('/', "_").upper()
        yield "CLASS_%s = %r" % (err, clscode)
    
    for clscode, clslabel in sorted(classes.items()):
        yield ""
        yield "# %s" % clslabel

        for errcode, errlabel in sorted(errors[clscode].items()):
            yield "%s = %r" % (errlabel, errcode)

if __name__ == '__main__':
    sys.exit(main())


