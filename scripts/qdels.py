#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def wildcard(string):

    string = string.strip("*").split("*")

    return string


def choose_task(line, key):

    taskid = ""
    task = line[2]


    for i in key:
        if i not in task:
            taskid = ""
            break
        taskid = line[0]

    return taskid


def read_qstat(string=""):

    if "*" in string.strip("*"):
        string = wildcard(string)
    else:
        string = [string]

    cmd = "qstat"
    result = os.popen(cmd)
    r = []

    for n, line in enumerate(result):
        line = line.strip()
        if line.startswith("#") or not line or line.startswith("---") or line.startswith("job-ID"):
            continue

        line = line.split()
        taskid = choose_task(line, string)
        if taskid:
            r.append(taskid)

    return r


def qdel_task(string):

    taxids = read_qstat(string)

    for i in taxids:
        cmd = "qdel %s" % i
        result = os.popen(cmd)

    return 0


def add_help_args(parser):

    parser.add_argument("-k", "--keyword", metavar="STR", type=str, default="",
        help="Input the keyword for the task (wildcards are supported).")

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
    qdels.py: Batch clean up specified tasks.

attention:
    qdels.py -k evm_*
    qdels.py

version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()

    qdel_task(args.keyword)


if __name__ == "__main__":

    main()
