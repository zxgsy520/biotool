#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import gzip
import pysam
import logging
import argparse

import numpy as np

LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


HEADER = {'HD': {'VN':'1.5', 'SO':'unknown', 'pb':'3.0.5'},
    'RG': [{'ID':'81e78fab', 'PL':'PACBIO',
        'DS':'READTYPE=SUBREAD;Ipd:CodecV1=ip;PulseWidth:CodecV1=pw;BINDINGKIT=101-365-900;SEQUENCINGKIT=101-309-500;BASECALLERVERSION=5.0.0;FRAMERATEHZ=80.00',
        'PU':'m54136_181127_023333', 'PM':'SEQUEL'},
        {'ID':'baz2bam', 'PN':'baz2bam', 'VN':'6.0.0.47712'},
        {'ID':'bazFormat', 'PN':'bazformat', 'VN':'1.5.0'},
        {'ID':'bazwriter', 'PN':'bazwriter', 'VN':'6.0.0.47712'}]}


TAGS = (('cx', 2),
    ('qe', 18980),
    ('qs', 5863),
    ('rq', 0.80),
    ('sn', ('f', (7.66, 14.48, 5.90, 9.68))),
    ('zm', 4194437),
    ('RG', '81e78fab'))


def read_fasta(file):
    '''Read fasta file'''

    if file.endswith(".gz"):
        fp = gzip.open(file)
    elif file.endswith(".fasta") or file.endswith(".fa"):
        fp = open(file)
    else:
        raise Exception("%r file format error" % file)

    seq = ''

    for line in fp:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()

        if not line:
            continue
        if not seq:
            seq += "%s\n" % line.strip(">").split()[0]
            continue
        if line.startswith(">"):
            line = line.strip(">").split()[0]
            seq = seq.split('\n')

            yield [seq[0], seq[1]]
            seq = ''
            seq += "%s\n" % line
        else:
            seq += line

    seq = seq.split('\n')
    if len(seq)==2:
        yield [seq[0], seq[1]]
    fp.close()


def read_fastq(file):
    '''Read fastq file'''

    if file.endswith(".gz"):
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
        if line.startswith('@') and (len(seq)==0 or len(seq)>=5):
            seq.append(line.strip("@").split()[0])
            continue
        if line.startswith('@') and len(seq)==4:
            yield seq
            seq = []
            seq.append(line.strip("@").split()[0])
        else:
            seq.append(line)

    if len(seq)==4:
        yield seq
    fp.close()


def fa2fq(file):

    if file.endswith(".fastq") or file.endswith(".fq") or file.endswith(".fastq.gz") or file.endswith(".fq.gz"):
        fp = read_fastq(file)
    else:
        fp = read_fasta(file)

    for line in fp:
        seqid = line[0]
        seq = line[1]
        quality = ""

        if len(line) == 4:
            quality = line[4]
        else:
            for i in range(len(seq)):
                quality += '!'
        yield seqid, seq, quality


def get_sample(file):

    name = file.split('/')[-1]

    if '--' in name:
        name = name.split('--')[1].split('.bam')[0]
    else:
        name = name.split('.')[0]

    return name


def fastp2bam(file, bam):

    if bam.endswith(".bam"):
        fh = pysam.AlignmentFile(bam, "rb", check_sq=False)
    elif bam.endswith(".sam"):
        fh = pysam.AlignmentFile(bam, 'r')
    else:
        raise Exception("%r file format error" % bam)

    name = get_sample(file)
    fo = pysam.AlignmentFile("%s.bam" % name, "wb", template=fh)
    print(fh.header)

    for line in fh:
        a = line
        #print(a.tags)
        break
    fh.close()

    for seqid, seq, quality in fa2fq(file):
        x = a
        x.query_name = seqid
        x.query_sequence = seq
        x.query_qualities = pysam.qualitystring_to_array(quality)
        #x.tags = TAGS
        fo.write(x)
    fo.close()


def add_hlep_args(parser):

    parser.add_argument('input', metavar='FILE', type=str,
        help='Input reads file, format(fastq, fasta).')
    parser.add_argument('-b', '--bam', metavar='FLIE', type=str, required=True,
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
name:
    fastp2bam

attention:
    fastp2bam nam.fastq -n name.bam
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    fastp2bam(args.input, args.bam)


if __name__ == "__main__":

    main()
