#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import logging
import argparse


LOG = logging.getLogger(__name__)

__version__ = "2.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def move_file(file, nfile):

    LOG.debug("mv %s %s" % (file, nfile))

    shutil.move(file, nfile)

    return 0


def copy_file(file, nfile):

    LOG.info("cp %s %s" % (file, nfile))

    shutil.copy(file, nfile)

    return 0


def check_path(path):

    path = os.path.abspath(path)

    if not os.path.exists(path):
        msg = "File not found '{path}'".format(**locals())
        LOG.error(msg)
        raise Exception(msg)

    return path


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


def move_files(file_path, path, prefix, oprefix=""):

    path = mkdir(path)
    file_path = check_path(file_path)
    rpath = "/".join(file_path.split("/")[0:-1])

    for root, dirs, files in os.walk(file_path):
        if not files:
            continue
        root = check_path(root)
        nroot = root.replace(rpath, path)
        nroot = mkdir(nroot)
        for file in files:
            if not oprefix:
                oprefix = file.split(".")[0]
            if oprefix not in file:
                nfile = file
            else:
                nfile = file.replace(oprefix, prefix)
            file = "%s/%s" % (root, file)
            nfile = "%s/%s" % (nroot, nfile)
            copy_file(file, nfile)

    return 0


def add_hlep_args(parser):

    parser.add_argument("-f", "--files", metavar='FILE', type=str, required=True,
        help="Input files.")
    parser.add_argument("--path", metavar='FILE', type=str, default='',
        help="The path where the input file needs to be moved.")
    parser.add_argument("-p", "--prefix", metavar='STR', type=str, default='out',
        help="Modified file prefix name， default=out")
    parser.add_argument("-op", "--old_prefix", metavar='STR', type=str, default='',
        help="File prefix name before modification")

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
    move_files.py Modify file prefix

attention:
    move_files.py --files ./ --prefix name
    move_files.py -f NPGAP.out/result/ --path ./ --prefix new --old_prefix JG-01
version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    move_files(args.files, args.path, args.prefix, args.old_prefix)


if __name__ == "__main__":

    main()
