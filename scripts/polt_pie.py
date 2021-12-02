#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse
import matplotlib
matplotlib.use('Agg')

import numpy as np
from matplotlib import pyplot as plt

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


COLOR = ['#080B74', '#303285', '#A63800', '#BF6030', '#91A200', '#ACBB2F', '#FFDB73', '#FFCE40',
     '#FFBE00', '#DFFA00', '#FF5600', '#1A1EB2', '#7375D8', '#4E51D8', '#FFA273',
     '#FF8040', '#EDFC72', '#E8FC3F', '#A67B00', '#BF9B30']


def read_tsv(file, sep=None):

    LOG.info("reading message from %r" % file)

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def tax_number(file):

    taxs = []
    numbers = []

    for line in read_tsv(file, "\t"):
        taxs.append(line[0])
        numbers.append(int(line[1]))

    return taxs, numbers


def polt_pie(data, label, prefix, sangle=120):

    #fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(aspect="equal"))
    plt.figure(figsize=(10, 5))
    ax =  plt.axes([0.18, 0.025, 0.50, 0.95])

    wedges, texts = ax.pie(data, wedgeprops= {'linewidth':0.5,'edgecolor':'white'}, startangle=sangle, colors=COLOR[0:len(data)])

    ax.legend(wedges, label,
        loc="upper left",
        frameon=False,
        fontsize="medium",
        labelspacing=0.3,
        handlelength=0.6,
        handleheight=0.6,
        handletextpad=0.3,
        bbox_to_anchor=(1.1, 0, 0.70, 1))

    note = []
    for i in range(len(data)):
        note.append('{0}({1:.2f}%)'.format(label[i], data[i]*100.0/sum(data)))

    bbox_props = dict(boxstyle="square,pad=0", fc="w", ec="0", lw=0)
    kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        if data[i]*100.0/sum(data) <1:
            continue
        ang = (p.theta2 - p.theta1)/2.0 + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})

        ax.annotate(note[i], xy=(x*0.95, y*0.95), xytext=(1.15*x, 1.15*y), #xytext=(1.35*np.sign(x), 1.4*y)
            horizontalalignment=horizontalalignment, fontsize=8, **kw)

    plt.savefig('%s.png' % prefix, dpi=700)
    plt.savefig("%s.pdf" % prefix)


def add_help_args(parser):

    parser.add_argument('input', metavar='FILE', type=str,
        help='Input file.')
    parser.add_argument('--sangle',  metavar='INT', type=int, default=120,
        help='Set the starting angle; default=120.')
    parser.add_argument('-p', '--prefix',  metavar='STR', type=str, default='out',
        help='Prefix of input and output results; default=out.')

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
     polt_pie.py Draw a pie chart

attention:
     polt_pie.py input.txt -p out
Input file format:
Lachnospiraceae	57299
Oscillospiraceae	33466
unclassified_Bacteria_family	21762
Clostridiaceae	18818
Muribaculaceae	14033
Bacteroidaceae	12512
unclassified_Eubacteriales_family	10247
unclassified_Firmicutes_family	7984
version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args = add_help_args(parser).parse_args()
    label, data = tax_number(args.input)

    polt_pie(data, label, args.prefix, args.sangle)


if __name__ == "__main__":

    main()
