#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import gzip
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_fastq(file):
    '''Read fastq file'''

    LOG.info("Reading message from %r" % file)
    if file.endswith("fastq.gz") or file.endswith(".fq.gz"):
        fp = gzip.open(file)
    elif file.endswith(".fastq") or file.endswith(".fq"):
        fp = open(file)
    else:
        raise Exception("%r file format error" % file)

    seq = []
    for line in fp:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()

        if not line:
            continue
        if not seq:
            seq.append(line.strip("@").split()[0])
            continue

        seq.append(line)
        if len(seq) == 4:
            yield seq
            seq = []

    fp.close()


def fq2fa(files, minlen):
    '''Convert fastq files to fasta files'''

    for file in files:
        for seqid, seq, ignore, quality in read_fastq(file):
            if len(seq) < minlen:
                LOG.info("The length of the filter sequence %s is %s" % (seqid, len(seq)))
                continue
            print('>%s\n%s' % (seqid, seq))

    return 0


def add_hlep_args(parser):

    parser.add_argument('fastq', nargs='+', metavar='FILE', type=str,
        help='Input fastq file.')
    parser.add_argument('--minlen', metavar='INT', type=int, default=0,
        help='Set the minimum length of sequence filtering, default=0')
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
    fq2fa.py -- Convert fastq files to fasta files

attention:
    fq2fa.py data.fastq >data.fasta
    fq2fa.py data.fastq --minlen 500 >data.fasta
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    fq2fa(args.fastq, args.minlen)


if __name__ == "__main__":
    main()
