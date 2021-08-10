#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import hashlib
import logging
import argparse


LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def search_md5(file):

    md = hashlib.md5()
    fh = open(file, 'rb')

    md.update(fh.read())
    fh.close()

    return md.hexdigest()


def check_path(path):

    path = os.path.abspath(path)

    if not os.path.exists(path):
        msg = "File not found '{path}'".format(**locals())
        LOG.error(msg)
        raise Exception(msg)

    return path


def make_md5(fpath):

    for root, dirs, files in os.walk(fpath):
        if not files:
            continue
        for file in files:
            file_name = os.path.join(root, file)
            file = check_path(file_name)
            file_md5 = search_md5(file)
            print("%s\t%s" % (file_md5, file_name))

    return 0


def make_md5s(fpaths):

    for i in fpaths:
        make_md5(i)

    return 0


def add_hlep_args(parser):

    parser.add_argument("files", nargs='+', metavar='FILE', type=str,
        help="Input files.")
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
    makemd5.py Generate MD5 values for files in the folder one by one

attention:
    makemd5.py ./ > result.md5
    makemd5.py genomic.fasta > result.md5
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    make_md5s(args.files)


if __name__ == "__main__":

    main()
