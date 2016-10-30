#!/usr/bin/env python3


import sys
import Standardize

def main(args):
    input = args[1]
    Standardize.standardize(input)

arguments = sys.argv
main(arguments)
