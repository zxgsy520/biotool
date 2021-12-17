#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import pysam
import logging
import argparse


LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_id(file):

    LOG.info("reading message from %r" % file)

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split()[0]


def get_bam(bam, id, out):

    idlist = set()

    for i in read_id(id):
        idlist.add(i)

    fh = pysam.AlignmentFile(bam, "rb", check_sq=False)
    fo = pysam.AlignmentFile(out, "wb", template=fh)

    for line in fh:
        if line.qname not in idlist:
            continue
        fo.write(line)
    fh.close()
    fo.close()


def add_hlep_args(parser):

    parser.add_argument('bam',
        help='Input reads file, format(bam and sam).')
    parser.add_argument('-id', '--seqids', metavar='FILE', type=str, required=True,
        help='List of input sequence ids.')
    parser.add_argument('-o', '--out', metavar='FILE', type=str, default='out.bam',
        help='The name of the output file, default=out.bam.')

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
    get_bam.py Get a specific sequence in bam.

attention:
    get_bam.py input.bam -id seq.id -o output.bam

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    get_bam(args.bam, args.seqids, args.out)


if __name__ == "__main__":

    main()
