#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import gzip
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.2.2"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def convert_size(string):

    size = string.lower()

    if size.endswith("g") or size.endswith("gb"):
        size, unit = size.split("g", 1)
        size = float(size)*1e9
    elif size.endswith("m") or size.endswith("mb"):
        size, unit = size.split("m", 1)
        size = float(size)*1e6
    elif size.endswith("k") or size.endswith("kb"):
        size, unit = size.split("k", 1)
        size = float(size)*1e3
    else:
        try:
            size = float(size)
        except:
            raise Exception("Size %s input error" % string)

    return size


def get_prefix(file):

    file = file.split('/')
    prefix = file[-1].split('.')

    if prefix[-1] == "gz":
        prefix = prefix[:-2:]
    else:
        prefix = prefix[:-1:]

    return ".".join(prefix)


def mkdir(d):
    """
    from FALCON_KIT
    :param d:
    :return:
    """
    d = os.path.abspath(d)
    if not os.path.isdir(d):
        LOG.debug('mkdir {!r}'.format(d))
        os.makedirs(d)
    else:
        LOG.debug('mkdir {!r}, {!r} exist'.format(d, d))

    return d


def cut_seq(seq, binlen="50kb"):

    binlen = int(convert_size(binlen))
    seqlen = len(seq)
    seqid = ""

    for i in range(0, seqlen, binlen):
        start = i
        end = start+binlen
        if end >= seqlen:
            end = seqlen
        seqid = "%s_%s" % (start+1, end)
        yield [seqid, seq[start:end]]


def read_fasta(file):

    '''Read fasta file'''
    if file.endswith(".gz"):
        fp = gzip.open(file)
    elif file.endswith(".fasta") or file.endswith(".fa"):
        fp = open(file)
    else:
        raise Exception("%r file format error" % file)

    r = ""
    for line in fp:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()

        if not line:
            continue
        if line.startswith(">"):
            if r:
                yield r.split("\n", 1)
            r = "%s\n" % line.strip(">")
            continue
        r += line.upper()

    if r:
        yield r.split("\n", 1)
    fp.close()


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


def run_sort_genome(file, minlen=500):

    r = {}
    ds = {}
    n = 0

    for seqid, seq in read_fasta(file):
        n += 1
        if len(seq) <= minlen:
            continue
        r[seqid] = seq
        ds[seqid] = len(seq)

    sn = 0
    cn = 0
    #tig_format = "contig{:0>%s}" % len(str(n))
    #scaf_format = "scaffold{:0>%s}" % len(str(n))
    tig_format = "tig{:0>%s}" % len(str(n))
    scaf_format = "scf{:0>%s}" % len(str(n))
    for seqid, seqlen in sorted(ds.items(), key = lambda x:x[1], reverse=True):
        seq = r[seqid]
        if "N" in seq:
            sn += 1
            seqid = scaf_format.format(sn)
        else:
            cn += 1
            seqid = tig_format.format(cn)
        print('>%s\n%s' % (seqid, seq))

    return 0


def run_look_alnfa(file, ref=""):

    r = {}
    ids = []
    for seqid, seq in read_fasta(file):
        seqid = seqid.split()[0]
        r[seqid] = seq
        if seqid == ref:
            continue
        ids.append(seqid)

    if ref not in r:
        raise Exception("Reference sequence %s does not exist" % ref)
    head = "Position\t%s" % ref
    for i in ids:
        head += "\t%s\tSame" % i
    print(head)

    n = 0
    for i in r[ref]:
        n += 1
        temp = [str(n), i]
        for j in ids:
            base = r[j][n-1]
            jb = "N"
            if base == i:
                jb = "."
            temp += [base, jb]
        print("\t".join(temp))

    return 0


def look_alnfa(args):

    run_look_alnfa(args.align, args.ref)

    return 0



def run_fq2fa(files, minlen):
    '''Convert fastq files to fasta files'''

    for file in files:
        for seqid, seq, ignore, quality in read_fastq(file):
            if len(seq) < minlen:
                LOG.info("The length of the filter sequence %s is %s" % (seqid, len(seq)))
                continue
            print('>%s\n%s' % (seqid, seq))

    return 0


def cut_seqs(file, binlen, cut):

    if file.endswith(".fasta") or file.endswith(".fa") or file.endswith(".fasta.gz") or file.endswith(".fa.gz"):
        fp = read_fasta(file)
    elif file.endswith(".fastq") or file.endswith(".fq") or file.endswith(".fastq.gz") or file.endswith(".fq.gz"):
        fp = read_fastq(file)
    else:
        raise Exception("%r file format error" % file)

    for line in fp:
        if not cut:
            yield line
            continue
        line[0] = line[0].split()[0]
        for seqid, seq in cut_seq(line[1], binlen):
            seqid = "%s:%s" % (line[0], seqid)
            yield [seqid, seq]


def run_seqsplit(file, workdir, prefix, size, binlen, cut):

    size = convert_size(size)
    workdir = mkdir(workdir)
    format = "fa"

    if file.endswith(".fastq") or file.endswith(".fq") or file.endswith(".fastq.gz") or file.endswith(".fq.gz"):
        format = "fq"
    if cut:
        format = "fa"
    if prefix == "":
        prefix = get_prefix(file)

    n = 0
    lable = 1
    fo = open('{}/{}.part{}.{}'.format(workdir, prefix, lable, format), 'w')

    for line in cut_seqs(file, binlen, cut):
        if n >= size:
            fo.close()
            n = 0
            lable += 1
            fo = open('{}/{}.part{}.{}'.format(workdir, prefix, lable, format), 'w')
        if format == "fa":
            fo.write(">%s\n" % "\n".join(line))
        else:
            fo.write("@%s\n" % "\n".join(line))
        n += len(line[1])
    fo.close()


def add_sort_genome_args(parser):

    parser.add_argument('genome',
        help='Input genome file.')
    parser.add_argument('--minlen', metavar='INT', type=int, default=500,
        help='Set the shortest sequence length for filtering, default=500')

    return parser


def sort_genome(args):

    run_sort_genome(args.genome, args.minlen)

    return 0


def add_fq2fa_args(parser):

    parser.add_argument('fastq', nargs='+', metavar='FILE', type=str,
        help='Input fastq file.')
    parser.add_argument('--minlen', metavar='INT', type=int, default=0,
        help='Set the minimum length of sequence filtering, default=0')
    return parser


def fq2fa(args):

    run_fq2fa(files=args.fastq, minlen=args.minlen)

    return 0


def add_seqsplit_args(parser):

    parser.add_argument('input', metavar='FILE', type=str,
        help='Input sequence file, format(fastq, fasta, fastq.gz, fasta.gz)')
    parser.add_argument('-w', '--workdir', metavar='FILE', type=str, default='./',
        help='Set the output file path, default=./')
    parser.add_argument('-s', '--size', metavar='STR', type=str, default='10m',
        help='Split file size, default=10m')
    parser.add_argument('-p', '--prefix', metavar='STR', type=str, default='',
        help='Set the prefix of the output file, default=""')
    parser.add_argument("--cut", action="store_true",
        help="Sequence is cut.")
    parser.add_argument('-b', '--binlen', metavar='STR', type=str, default='50kb',
        help='The length of the sequence to be cut, default=50kb')

    return parser


def add_look_alnfa_args(parser):

    parser.add_argument('align', metavar='FILE', type=str,
        help='Input the aligned multi-sequence file(fasta).')
    parser.add_argument("-r", '--ref', metavar='STR', type=str, required=True,
        help='Input the id of the reference sequence')

    return parser


def seqsplit(args):

    run_seqsplit(file=args.input,
        workdir=args.workdir,
        prefix=args.prefix,
        size=args.size,
        binlen=args.binlen,
        cut=args.cut
    )

    return 0


def add_biotool_parser(parser):

    subparsers = parser.add_subparsers(
        title='command',
        dest='commands')
    subparsers.required = True

    fq2fa_parser = subparsers.add_parser('fq2fa', help="fastq to fasta")
    fq2fa_parser = add_fq2fa_args(fq2fa_parser)
    fq2fa_parser.set_defaults(func=fq2fa)

    seqsplit_parser = subparsers.add_parser('seqsplit',
        help="Split files by a specific size.")
    seqsplit_parser = add_seqsplit_args(seqsplit_parser)
    seqsplit_parser.set_defaults(func=seqsplit)

    sort_genome_parser = subparsers.add_parser('sort_genome',
        help="Sort and rename the genome.")
    sort_genome_parser = add_sort_genome_args(sort_genome_parser)
    sort_genome_parser.set_defaults(func=sort_genome)

    look_alnfa_parser = subparsers.add_parser('look_alnfa',
        help="View multiple sequence alignment files.")
    look_alnfa_parser = add_look_alnfa_args(look_alnfa_parser)
    look_alnfa_parser.set_defaults(func=look_alnfa)

    return parser


def main():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
name:
biotool：Commonly used processing tools for biological information

URL：https://github.com/zxgsy520/biotool

version: %s
contact:  %s <%s>\
        """ % (__version__, " ".join(__author__), __email__))

    parser = add_biotool_parser(parser)
    args = parser.parse_args()

    args.func(args)

    return parser.parse_args()


if __name__ == "__main__":

    main()
