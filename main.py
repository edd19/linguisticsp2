#!/usr/bin/env python3

import sys
import Standardize
import n_gram


def main(args):
    input = args[1]
    Standardize.standardize(input)
    lexicon = build_lexicon("output.txt")
    print(lexicon.get_size())
    print(lexicon.get_top_n_by_counts(20))


def build_lexicon(filepath):
    lexicon = n_gram.NGram()
    with open(filepath, "r") as file:
        for line in file:
            lexicon.add_corpus(line)
    return lexicon

arguments = sys.argv
main(arguments)
