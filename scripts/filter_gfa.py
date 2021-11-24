#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.2.1"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    LOG.info("reading message from %r" % file)
    fo = open(file)

    for line in fo:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)
    fo.close()


def gmk2pb(string):

    string = string.lower().strip()

    if string.endswith('g') or string.endswith('gb'):
        base = string.split('g')[0]
        base = float(base)*1e+09
    elif string.endswith('m') or string.endswith('mb'):
        base = string.split('m')[0]
        base = float(base)*1e+06
    elif string.endswith('k') or string.endswith('kb'):
        base = string.split('k')[0]
        base = float(base)*1e+03
    else:
        base = float(string)

    return int(base)


def get_value(string):

    string = string.split(":")

    return float(string[-1])


def read_attribute(file):

    r = {}

    for line in read_tsv(file, "\t"):
        if line[0]!="S":
            continue
        r[line[1]] = {"length": get_value(line[3]),
                      "depth": get_value(line[4])}

    return r


def filter_gfa(file, minlen, mindepth):

    r = read_attribute(file)
    seqid = set()
    minlen = gmk2pb(minlen)

    for line in read_tsv(file, "\t"):
        if line[0]=='S':
            attr = r[line[1]]
            if (attr["length"] <= minlen) or (attr["depth"] <= mindepth):
                continue
            seqid.add(line[1])
        elif line[0]=='L':
            if (line[1] not in seqid) or (line[3] not in seqid):
                continue
        else:
            pass
        print('\t'.join(line))

    return 0


def add_help(parser):

    parser.add_argument('gfa', metavar='FILE', type=str,
        help='Input file.')
    parser.add_argument('-ml', '--minlen', metavar='STR', type=str, default='1.5mb',
        help='Minimum length of filtering, default=1.5mb.')
    parser.add_argument('-md', '--mindepth', metavar='FLOAT', type=float, default=0,
        help='Minimum depth of filtering, default=0.')

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
name:
    filter_gfa.py Filter the assembled gfa file
attention:
    filter_gfa.py file.gfa --minlen 1.5mb >new.gfa
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_help(parser).parse_args()

    filter_gfa(args.gfa, args.minlen, args.mindepth)


if __name__ == "__main__":

    main()
