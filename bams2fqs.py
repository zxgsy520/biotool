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
__email__ = "113178210@qq.com"
__all__ = []


def read_bam(file):

    if file.endswith(".bam"):
        fh = pysam.AlignmentFile(file, "rb", check_sq=False)
    elif file.endswith(".sam"):
        fh = pysam.AlignmentFile(file, 'r')
    else:
        raise Exception("%r file format error" % file)

    for line in fh:
        #yield [line.qname, line.seq, pysam.array_to_qualitystring(line.query_qualities), line.get_tag('rq')]
        yield line.qname, line.seq, pysam.array_to_qualitystring(line.query_qualities)

    fh.close()


def bams2fqs(files):
    
    for file in files:
        name = file.split('/')[-1]
        if '--' in name:
            name = name.split('--')[1].split('.bam')[0]
        else:
            name = name.split('.')[0]

        fp = open("%s.fastq" % name, 'w')
        for seqid, seq, quality  in read_bam(file):
            fp.write('@%s\n%s\n+\n%s\n' % (seqid, seq, quality))
        fp.close()


def add_hlep_args(parser):

    parser.add_argument('bam', nargs='+', metavar='FILE', type=str,
        help='Input reads file, format(bam and sam).')

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
URL: https://github.com/zxgsy520/sbarcode
name:
    bams2fqs.py Convert bam file to fastq file.
     
attention:
    bams2fqs.py *.bam

version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    bams2fqs(args.bam)


if __name__ == "__main__":

    main()
