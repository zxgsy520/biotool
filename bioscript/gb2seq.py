#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse

from Bio import SeqIO

LOG = logging.getLogger(__name__)

__version__ = "v1.2.1"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def gb2seq(file, types, table):
    """
    Read the genbank file.
    Export gene sequences,
    protein sequences and genes from newly named genes.
    """
    LOG.info("reading message from %r" % file)

    if file.endswith(".gz"):
        fh = gzip.open(file)
    else:
        fh = open(file)

    temp = ""
    if types == "pep":
        temp = "pep"
        types = "CDS"

    for record in SeqIO.parse(fh, "genbank"):
        for gene_dict in record.features:
            if gene_dict.type != types:
                continue
            seq = gene_dict.extract(record.seq)

            if "note" not in gene_dict.qualifiers:
                note = ""
            else:
                note = gene_dict.qualifiers["note"][0]

            gene = str(gene_dict.qualifiers["gene"][0])
            if temp:
                if "translation" in gene_dict.qualifiers:
                    seq = str(gene_dict.qualifiers["translation"][0])
                else:
                    seq = str(seq.translate(table=table))

            print(">%s %s\n%s" % (gene, note, seq))

    return 0


def gb2seqs(files, types="CDS", table=11):

    for file in files:
        gb2seq(file, types, table)

    return 0


def add_help_args(parser):

    parser.add_argument("genbank", metavar="FILE", type=str, nargs='+',
        help="Input genebank file containing protein sequence.")
    parser.add_argument("-tp", "--types", metavar="STR", type=str, default="CDS",
        choices=["CDS", "rRNA", "tRNA", "gene", "pep"],
        help="Input sequence type(CDS, rRNA, tRNA, gene, pep), default=CDS")
    parser.add_argument("-t", "--table", metavar="INT", type=int, default=11,
        help="Input codon table used, default=11")

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
name:
     gb2seqs.py Get sequences from genebank files.

attention:
     gb2seqs.py genomic.gb -tp CDS > CDS.fa

version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()

    gb2seqs(args.genbank, args.types, args.table)


if __name__ == "__main__":

    main()
