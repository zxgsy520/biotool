#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gzip
import os.path
import logging
import argparse
import collections

from Bio import SeqIO
from multiprocessing import Pool

LOG = logging.getLogger(__name__)

__version__ = "v1.2.1"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def mkdir(d):
    """
    from FALCON_KIT
    :param d:
     :return:
    """
    d = os.path.abspath(d)
    if not os.path.isdir(d):
        LOG.debug("mkdir {!r}".format(d))
        os.makedirs(d)
    else:
        LOG.debug("mkdir {!r}, {!r} exist".format(d, d))

    return d


def get_prefix(file):

    file = file.split("/")[-1]

    if "." in file:
        prefix = file.split(".")[0]
    else:
        prefix = file

    return prefix


def reads_gb(file, filter):
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

    if file.endswith(".gbff.gz") or file.endswith(".gb.gz") or file.endswith(".gbff") or  file.endswith(".gb"):
        fh = SeqIO.parse(fh, "genbank")
    else:
        raise Exception("Unknown format!")

    for record in fh:
        for genes in record.features :
            gene_seq = genes.extract(record.seq)

            if genes.type != "CDS":
                continue

            gene_desc = genes.qualifiers
            if "locus_tag" in gene_desc:
                gene_id = genes.qualifiers["locus_tag"][0]
            elif "gene" in gene_desc:
                gene_id = genes.qualifiers["gene"][0]
            elif "protein_id" in gene_desc:
                gene_id = genes.qualifiers["protein_id"][0]
            else:
                gene_id = ""
            if filter:
                if len(gene_seq) % 3 != 0:
                    LOG.info("The length of gene %s is not a multiple of 3" % gene_id)
                    continue
                if len(gene_seq) <= 45:     
                    LOG.info("Gene %s length is less than 45bp" % gene_id)

            try:
                protein = str(genes.qualifiers["translation"][0])
                cds = str(gene_seq)
            except:
                protein = str(gene_seq.translate(table=11))
                LOG.info("Gene %s no protein sequence" %  gene_id)
                #continue

            yield cds, protein, gene_id


def gb2cod_seq(file, output, rename=None, filter=None):

    """
    Output cds file, protein sequence file and name corresponding file
    """
    prefix = get_prefix(file)
    fc = open(os.path.join(output, "%s.cds.fa" % prefix), "w")
    fp = open(os.path.join(output, "%s.pep.fa" % prefix), "w")
    fn = open(os.path.join(output, "%s.rename.tsv" % prefix), "w")

    n = 0
    fn.write("#Old name\tNew name\n")
    for cds, pep, seqid in reads_gb(file, filter):
        n += 1
        if rename:
            new_seqid = "%s|cds_%s" % (prefix, n)
        else:
            new_seqid = seqid

        fc.write(">%s\n%s\n" % (new_seqid, cds))
        fp.write(">%s\n%s\n" % (new_seqid, pep))
        fn.write("%s\t%s\n" % (seqid, new_seqid))

    fc.close()
    fp.close()
    fn.close()

    return [prefix, n, os.path.join(output, "%s.pep.fa" % prefix)]


def gb2cod_seqs(files, thread, output, rename, filter):

    output = mkdir(output)
    pool = Pool(processes=thread)
    results = []

    for file in files:
        results.append(pool.apply_async(gb2cod_seq, (file, output, rename, filter)))

    pool.close()
    pool.join()

    fo = open("sp.list", "w")
    for i, r in enumerate(results):
        line = r.get()
        print("%s\t%s" % (line[0], line[2]))
        fo.write("%s\t%s\n" % (line[0], line[1]))
    fo.close()


def add_help_args(parser):

    parser.add_argument("input", nargs="+", metavar='FILE', type=str,
        help="Input genebank files")
    parser.add_argument("-t", "--thread", metavar="INT", type=int, default=1,
        help="Set the number of threads, default=1")
    parser.add_argument("-o", "--out", metavar="FILE", type=str, default="out",
        help="Input result output path, default=./out")
    parser.add_argument("--rename", action="store_true", default=False,
        help="Rename the sequence, default=False.")
    parser.add_argument("--filter", action="store_true", default=False,
        help="Filter sequence, default=False.")


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
     gb2cds.py Get the correct cds and protein sequences from the gengbank file

attention:
     gb2cds.py *.gb -t 4 -o out

version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()

    gb2cod_seqs(args.input, args.thread, args.out, args.rename, args.filter)


if __name__ == "__main__":

    main()
