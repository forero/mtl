#!/usr/bin/env python

from __future__ import print_function, division

from mtl.initialize import new_observations_file
from mtl.initialize import new_results_file
from argparse import ArgumentParser
import os.path

#from mtl.initialize import results


ap = ArgumentParser()
ap.add_argument("src_target", help="Targets file")
ap.add_argument("src_observations", help="Observations file")
ap.add_argument("src_results", help="Results file")
ap.add_argument("dest", help="Output MTL")
ap.add_argument('-v', "--verbose", action='store_true')

def main():
    ns = ap.parse_args()
    #if the observations file does not exist, it makes an initialization
    if(not os.path.exists(ns.src_observations)):
        if ns.verbose:
            print("Initializing observations file {}".format(ns.src_observations))
        new_observations_file(ns.src_target, ns.src_observations)

    if(not os.path.exists(ns.src_results)):
        if ns.verbose:
            print("Initializing results file {}".format(ns.src_results))
        new_results_file(ns.src_target, ns.src_results)

if __name__=="__main__":
    main()

