#!/usr/bin/env python3

from estimation_n_grams import MaxLikelihood
from n_gram import Unigram


class LaplaceSmoothing(MaxLikelihood):
    def __init__(self, n=1):
        self.vocabulary = Unigram()
        super(self.__class__, self).__init__(n=n)

    def add_training_corpus(self, corpus):
        self.vocabulary.add_corpus(corpus)
        super(self.__class__, self).add_training_corpus(corpus)

    def compute_probability(self, ngram):
        count_n_gram = self.get_n_gram_count(ngram)
        count_n_minus_gram = self.get_n_minus_gram_count(ngram)
        vocabulary_size = self.vocabulary.get_size()
        if self.n == 1:
            return (count_n_gram + 1) / (self.n_grams.get_word_occurences() + vocabulary_size)
        else:
            return (count_n_gram + 1) / (count_n_minus_gram + vocabulary_size)

    def flush(self):
        self.vocabulary.flush()
        super(self.__class__, self).flush()
