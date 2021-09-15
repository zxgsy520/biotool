#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import gzip
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


TELOMERES = ["C{2,4}T{1,2}A{1,3}", "T{1,3}A{1,2}G{2,4}"]


def match_telomere(sequence, telomeres, number=5):

    telomere = False
    repeat = ""
    n = 0

    for i in range(len(telomeres)-number):

        repeat = "".join(telomeres[i:i+number])
        if repeat not in sequence:
            continue
        telomere = True

        temp = repeat
        n = number
        for j in range((i+number+1), len(telomeres)):
            temp = "".join(telomeres[i:j])
            if temp not in sequence:
                break
            n += 1
            repeat = temp
        break

    return telomere, repeat, n


def complement(seq):

    cdict = {"A": "T",
        "T": "A",
        "G": "C",
        "C": "G"
    }

    seq = list(seq.upper())
    nseq = ""
    for i in seq:
        nseq += cdict[i]

    return nseq


def reverse_complement(seq):

    seq = seq[::-1]

    return complement(seq)


def find_telomere(sequence, tel_seq="", repeats=5):

    if tel_seq:
        ftel = tel_seq
        rtel = reverse_complement(tel_seq)
    else:
        ftel = TELOMERES[0]
        rtel = TELOMERES[1]

    forwards = re.findall(ftel, sequence)
    ftelomere, frepeat, fnumber =  match_telomere(sequence, forwards, repeats)
    reverses = re.findall(rtel, sequence)
    rtelomere, rrepeat, rnumber =  match_telomere(sequence, reverses, repeats)

    return ftelomere, frepeat, fnumber, rtelomere, rrepeat, rnumber


def read_fasta(file):

    '''Read fasta file'''
    if file.endswith(".gz"):
        fp = gzip.open(file)
    elif file.endswith(".fasta") or file.endswith(".fa"):
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
        if line.startswith(">"):
            line = line.strip(">")
            if len(seq) == 2:
                yield seq
            seq = []
            seq.append(line.split()[0])
            continue
        if len(seq) == 2:
            seq[1] += line
        else:
            seq.append(line)

    if len(seq) == 2:
        yield seq
    fp.close()


def find_telomeres(file, tel_seq="", repeats=5):

    print("#Seq_id\tStrand\tRepeat number\tTelomere")
    for seqid, seq in read_fasta(file):
        seq = seq.upper()
        if len(seq)>=1000000:
           seq = seq[0:500000]+seq[len(seq)-500000::]
        ftelomere, frepeat, fnumber, rtelomere, rrepeat, rnumber = find_telomere(seq, tel_seq, repeats)
        if ftelomere:
            print("%s\tForward\t%s\t%s" %(seqid, fnumber, frepeat))
        if rtelomere:
            print("%s\tReverse\t%s\t%s" %(seqid, rnumber, rrepeat))
    return 0


def add_hlep_args(parser):

    parser.add_argument('fasta', metavar='FILE', type=str,
        help='Input genome sequence(fasta, fa, fasta.gz).')
    parser.add_argument('-t','--telomere', metavar='STR', type=str, default='',
        help='Input the telomere sequence, default=CCCTAA.')
    parser.add_argument('-r','--repeats', metavar='INT', type=int, default=5,
        help='Telomere Repeats, default=5.')

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
    find_telomeres.py Discover the telomere sequence from the genome

attention:
    find_telomeres.py genome.fasta > telomere.txt
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    find_telomeres(args.fasta, args.telomere, args.repeats)


if __name__ == "__main__":

    main()
