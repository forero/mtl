#!/usr/bin/env python

from __future__ import print_function, division

from mtl.initialize import new_specresults_file
from mtl.merge import create_mtl
from argparse import ArgumentParser
import os.path

#from mtl.initialize import results


ap = ArgumentParser()
ap.add_argument("src_target", help="Targets file")
ap.add_argument("src_specresults", help="Spectrographic results file")
ap.add_argument("dest", help="Output MTL")
ap.add_argument('-v', "--verbose", action='store_true')

def main():
    ns = ap.parse_args()

    #if the results file does not exist, it makes an initialization
    if(not os.path.exists(ns.src_specresults)):
        if ns.verbose:
            print("Initializing spec results file {}".format(ns.src_specresults))
        new_specresults_file(ns.src_target, ns.src_specresults)

    # from the targets, observations and results file, creates the mtl
    create_mtl(ns.src_target, ns.src_specresults, ns.dest)
    
if __name__=="__main__":
    main()

