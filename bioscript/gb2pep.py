#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse

from Bio import SeqIO

LOG = logging.getLogger(__name__)

__version__ = "v1.2.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def gb2pep(file):
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

    for record in SeqIO.parse(fh, "genbank"):
        organism = record.annotations["organism"]

        for gene_dict in record.features:
            if "organism" in gene_dict.qualifiers:
                organism = gene_dict.qualifiers["organism"][0]

            if "translation" not in gene_dict.qualifiers:
                continue
            protein = str(gene_dict.qualifiers["translation"][0])

            if "note" not in gene_dict.qualifiers:
                note = ""
            else:
                note = gene_dict.qualifiers["note"][0]

            gene = str(gene_dict.qualifiers["gene"][0])
            if "protein_id" in gene_dict.qualifiers:
                proteinid = str(gene_dict.qualifiers["protein_id"][0])
            else:
                proteinid = gene         

            desc = "%s OS=%s GN=%s" % (note, organism, gene)
            print(">%s %s\n%s" % (proteinid, desc.strip(), protein))

    return 0


def gb2peps(files):
    
    for file in files:
        gb2pep(file)

    return 0


def add_help_args(parser):

    parser.add_argument("genbank", metavar="FILE", type=str, nargs='+',
        help="Input genebank file containing protein sequence.")

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
     gb2pep.py Get protein sequences from genebank files.

attention:
     gb2pep.py genomic.gb >pep.fa

version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()

    gb2peps(args.genbank)


if __name__ == "__main__":

    main()
