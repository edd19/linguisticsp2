#!/usr/bin/env python3

import sys
import Standardize
import estimation_n_grams
import n_gram
from collections import Counter

OUTPUT_FILE = "output.txt"
OUTPUT_FILE_PROPER = "output2.txt"


def main(args):
    input = args[1]

    #Standardize.standardize(input, "output.txt")
    #
    # lexicon = build_lexicon(OUTPUT_FILE)
    # removed_words = lexicon.discard_unfrequent_n_grams(2)
    #
    # replace_removed_words(removed_words)

    # lexicon = build_lexicon(OUTPUT_FILE_PROPER)
    # print(lexicon.get_size())
    # print(lexicon.get_top_n_by_counts(20))

    # unigram, bigram, trigram = build_gram(OUTPUT_FILE_PROPER)
    # save_ngram_count(unigram, "./counts/unigram_counts.txt")
    # save_ngram_count(bigram, "./counts/bigram_counts.txt")
    # save_ngram_count(trigram, "./counts/trigram_counts.txt")

    #Standardize.standardize(input, "output3.txt")

    laplace = estimation_n_grams.LaplaceSmoothing()
    build_trainig(laplace, "output2.txt")
    build_test(laplace, "output3.txt")
    print(laplace.get_perplexity())

    linear = estimation_n_grams.LinearInterpolation(n=3, k=3)
    build_trainig(linear, "output2.txt")
    build_test(linear, "output3.txt")
    print(linear.get_perplexity())


def build_trainig(obj_estimation, filepath):
    with open(filepath, "r") as file:
        for line in file:
            obj_estimation.add_training_corpus(line)


def build_test(obj_estimation, filepath):
    with open(filepath, "r") as file:
        for line in file:
            obj_estimation.add_test_corpus(line)


def build_lexicon(filepath):
    lexicon = n_gram.NGram()
    with open(filepath, "r") as file:
        for line in file:
            lexicon.add_corpus(line)
    return lexicon


def build_gram(filepath):
    unigram = n_gram.NGram(1)
    bigram = n_gram.NGram(2)
    trigram = n_gram.NGram(3)
    with open(filepath, "r") as file:
        for line in file:
            unigram.add_corpus(line)
            bigram.add_corpus(line)
            trigram.add_corpus(line)
    return unigram, bigram, trigram


def save_ngram_count(ngram_obj, filepath):
    with open(filepath, "w") as file_to_write:
        counts = ngram_obj.get_counts().values()
        counts = Counter(counts)
        for (element, cnt) in counts.items():
            file_to_write.write(str(element) + "\t" + str(cnt))
            file_to_write.write("\n")


def replace_removed_words(removed_words):
    with open(OUTPUT_FILE, "r") as file:
        s = file.read()
        for removed_word in removed_words:
            s = s.replace(removed_word, " <UNK> ")
        with open(OUTPUT_FILE_PROPER, "w") as file_to_write:
            file_to_write.write(s)


arguments = sys.argv
main(arguments)
