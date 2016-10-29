#!/usr/bin/env python3

import n_gram
import math


class LinearInterpolation(object):
    def __init__(self, n=1, k=1):
        self.n = n
        self.k = k
        self.n_grams_array = self.create_n_grams_array()
        self.vocabulary = n_gram.NGram(1)
        self.cache = {}
        self.m = 0
        self.perplexity = 1

    def create_n_grams_array(self):
        n_grams_array = []
        for x in range(self.n, self.n-self.k, -1):
            n_grams_array.append((n_gram.NGram(x)))
        if self.n > self.k:
            n_grams_array.append(n_gram.NGram(self.n-self.k))
        return n_grams_array

    def add_training_corpus(self, corpus):
        self.vocabulary.add_corpus(corpus)
        for ngram in self.n_grams_array:
            ngram.add_corpus(corpus)

    def estimate_n_gram(self, ngram):
        probability = self.cache.get(ngram, None)
        if probability:
            return probability
        probability = self.compute_probability(ngram)
        self.cache[ngram] = probability
        return probability

    def compute_probability(self, ngram):
        probability = 0
        reduced_ngram = ngram
        for x in range(self.n - 1, self.n-self.k-1, -1):
            if x <= 0:
                probability += (1/self.k) * self.compute_probability_of_unigram(reduced_ngram)
            else:
                probability += (1/self.k) * self.compute_probability_of_n_gram(reduced_ngram, x+1, x)
            reduced_ngram = self.reduce_sentence(reduced_ngram)
        return probability

    @staticmethod
    def reduce_sentence(sentence):
        return " ".join(sentence.split()[1:])

    def compute_probability_of_n_gram(self, ngram, n, n_minus):
        count_n_gram = self.get_n_gram_count(ngram, n)
        count_n_minus_gram = self.get_n_minus_gram_count(ngram, n_minus)
        if count_n_minus_gram == 0:
            return 0
        else:
            return count_n_gram / count_n_minus_gram

    def compute_probability_of_unigram(self, word):
        count_word = self.get_n_gram_count(word, 1)
        occurences_words = self.get_occurences_words()
        return count_word / occurences_words

    def get_occurences_words(self):
        return self.vocabulary.get_word_occurences()

    def get_n_gram_count(self, ngram, n):
        return self.n_grams_array[self.n-n].get_n_gram_count(ngram)

    def get_n_minus_gram_count(self, ngram, n_minus):
        n_minus_gram = self.get_minus_n_gram(ngram)
        count_n_minus_grams = self.get_n_gram_count(n_minus_gram, n_minus)
        return count_n_minus_grams

    @staticmethod
    def get_minus_n_gram(ngram):
        words = ngram.split()
        n_minus_gram = " ".join(words[:-1])
        return n_minus_gram

    def flush(self):
        for ngram in self.n_grams_array:
            ngram.flush()
        self.cache.clear()
        self.vocabulary.flush()

    def add_test_corpus(self, corpus):
        for ngram in self.get_n_grams(corpus):
            probability = self.compute_probability(ngram)
            self.perplexity *= 1 / probability
            self.m += 1

    def get_perplexity(self):
        return math.pow(self.perplexity, 1/self.m)

    def get_n_grams(self, corpus):
        for sentence in self.split_corpus_sentences(corpus):
            for ngram in self.split_sentence_n_grams(sentence, self.n):
                yield ngram

    @staticmethod
    def split_corpus_sentences(corpus):
        corpus_left = corpus
        separator = "</s>"  # Signify end of sentence
        while len(corpus_left) > 0:
            sentence, sep, corpus_left = corpus_left.partition(separator)
            sentence += separator
            yield sentence.strip()

    @staticmethod
    def split_sentence_n_grams(sentence, n):
        words = sentence.split()
        n_grams = []
        for word in words:
            n_grams.append(word)
            if len(n_grams) >= n:
                yield " ".join(n_grams)
                n_grams.pop(0)


class MaxLikelihood(LinearInterpolation):
    def __init__(self, n=1):
        super(MaxLikelihood, self).__init__(n=n, k=1)


class LaplaceSmoothing(MaxLikelihood):
    def compute_probability_of_n_gram(self, ngram, n, n_minus):
        count_n_gram = self.get_n_gram_count(ngram, n)
        count_n_minus_gram = self.get_n_minus_gram_count(ngram, n_minus)
        vocabulary_size = self.vocabulary.get_size()
        return (count_n_gram + 1) / (count_n_minus_gram + vocabulary_size)

    def compute_probability_of_unigram(self, word):
        count_word = self.get_n_gram_count(word, 1)
        occurences_words = self.get_occurences_words()
        vocabulary_size = self.vocabulary.get_size()
        return (count_word + 1) / (occurences_words + vocabulary_size)


