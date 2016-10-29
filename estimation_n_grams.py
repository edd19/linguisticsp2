#!/usr/bin/env python3

import n_gram


class MaxLikelihood(object):
    def __init__(self, n=1):
        self.n_grams = n_gram.NGram(n)
        self.n_minus_1_grams = None
        if n > 1:
            self.n_minus_1_grams = n_gram.NGram(n-1)
        self.n = n
        self.cache = {}

    def add_training_corpus(self, corpus):
        self.n_grams.add_corpus(corpus)
        if self.n > 1:
            self.n_minus_1_grams.add_corpus(corpus)

    def estimate_n_gram(self, ngram):
        probability = self.cache.get(ngram, None)
        if probability:
            return probability
        probability = self.compute_probability(ngram)
        self.cache[ngram] = probability
        return probability

    def compute_probability(self, ngram):
        count_n_gram = self.get_n_gram_count(ngram)
        count_n_minus_gram = self.get_n_minus_gram_count(ngram)
        if self.n == 1:
            return count_n_gram / self.n_grams.get_word_occurences()
        elif count_n_minus_gram == 0:
            return 0
        else:
            return count_n_gram / count_n_minus_gram

    def get_n_gram_count(self, ngram):
        return self.n_grams.get_n_gram_count(ngram)

    def get_n_minus_gram_count(self, ngram):
        count_n_minus_grams = 0
        if self.n > 1:
            n_minus_gram = self.get_minus_n_gram(ngram)
            count_n_minus_grams = self.n_minus_1_grams.get_n_gram_count(n_minus_gram)
        return count_n_minus_grams

    @staticmethod
    def get_minus_n_gram(ngram):
        words = ngram.split()
        n_minus_gram = " ".join(words[:-1])
        return n_minus_gram

    def flush(self):
        self.n_grams.flush()
        if self.n > 1:
            self.n_minus_1_grams.flush()
        self.cache.clear()


class LaplaceSmoothing(MaxLikelihood):
    def __init__(self, n=1):
        self.vocabulary = n_gram.Unigram()
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
