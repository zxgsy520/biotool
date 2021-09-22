#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep="None"):

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def read_id(file):

    r = []

    for line in read_tsv(file):
        r.append(line[0])

    return r


def read_attr(attributes):

    r = {}

    for attribute in attributes.split(";"):
        tag, value = attribute.split('=', 1)
        r[tag] = value

    return r


def get_id(attr):

    seqid = ""

    if "ID" in attr:
        seqid = attr["ID"]
    elif "Parent" in attr:
        seqid = attr["Parent"]
    else:
        pass

    return seqid


def grep_gff(gids, gff, types="CDS"):

    ids = read_id(gids)
    
    for line in read_tsv(gff, "\t"):
        if line[2] != types:
            continue

        attr = read_attr(line[-1])
        seqid = get_id(attr)
        if seqid not in ids:
            continue
        print("\t".join(line))
        
    return 0


def add_hlep_args(parser):

    parser.add_argument('gids', metavar='FILE', type=str,
        help='Input sequence id file')
    parser.add_argument('-g', '--gff', metavar='FILE', type=str, required=True,
        help='Gff file of input sequence')
    parser.add_argument('-t', '--types', choices=["CDS", "gene", "rRNA", "tRNA"], default="CDS",
        help='Input the type of extraction sequence, default=CDS')

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
    grep_gff: Extract the annotation information in the gff file according to the sequence id.
attention:
    grep_gff cds.id -g genomic.gff3 >new.gff3
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    grep_gff(args.gids, args.gff, args.types)


if __name__ == "__main__":

    main()
